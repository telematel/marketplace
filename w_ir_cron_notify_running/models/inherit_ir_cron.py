# -*- encoding: utf-8 -*-
#
# Module written to Odoo, Open Source Management Solution
#
# Copyright (c) 2020 Wedoo - http://www.wedoo.tech/
# All Rights Reserved.
#
# Developer(s): Randy La Rosa Alvarez
#               (rra@wedoo.tech)
#
########################################################################
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import logging
import threading
import psycopg2
from datetime import datetime, timedelta
import odoo
from odoo import api, fields, models, _
BASE_VERSION = odoo.modules.load_information_from_description_file('base')['version']
MAX_FAIL_TIME = timedelta(hours=5)  # chosen with a fair roll of the dice


class BadVersion(Exception):
    pass


class BadModuleState(Exception):
    pass


_logger = logging.getLogger(__name__)


class IrCron(models.Model):
    _inherit = "ir.cron"

    running = fields.Boolean(
        default=False
    )

    @api.multi
    def set_all_cron_running_off(self):
        for cron in self:
            cron.running = False

    @api.multi
    def method_direct_trigger(self):
        self.check_access_rights('write')
        for cron in self:
            try:
                cron.running = True
                title = _('Cron notification.')
                msg = _('The cron %s has started.') % cron.name
                self.env.user.notify_default(title=title, message=msg)
                self._cr.commit()
                self.env['ir.actions.server'].browse(
                    cron.ir_actions_server_id.id).run()
            finally:
                cron.running = False
                title = _('Cron notification.')
                msg = _('The cron %s has finished.') % cron.name
                self.env.user.notify_default(title=title, message=msg)
        return True

    @classmethod
    def _process_jobs(cls, db_name):
        """ Try to process all cron jobs.

        This selects in database all the jobs that should be processed. It then
        tries to lock each of them and, if it succeeds, run the cron job (if it
        doesn't succeed, it means the job was already locked to be taken care
        of by another thread) and return.

        :raise BadVersion: if the version is different from the worker's
        :raise BadModuleState: if modules are to install/upgrade/remove
        """
        db = odoo.sql_db.db_connect(db_name)
        threading.current_thread().dbname = db_name
        try:
            with db.cursor() as cr:
                # Make sure the database has the same version as the code of
                # base and that no module must be installed/upgraded/removed
                cr.execute(
                    "SELECT latest_version FROM ir_module_module WHERE name=%s",
                    ['base'])
                (version,) = cr.fetchone()
                cr.execute(
                    "SELECT COUNT(*) FROM ir_module_module WHERE state LIKE %s",
                    ['to %'])
                (changes,) = cr.fetchone()
                if version is None:
                    raise BadModuleState()
                elif version != BASE_VERSION:
                    raise BadVersion()
                # Careful to compare timestamps with 'UTC' - everything is UTC as of v6.1.
                cr.execute("""SELECT * FROM ir_cron
                                  WHERE numbercall != 0
                                      AND active AND nextcall <= (now() at time zone 'UTC')
                                  ORDER BY priority""")
                jobs = cr.dictfetchall()

            if changes:
                if not jobs:
                    raise BadModuleState()
                # nextcall is never updated if the cron is not executed,
                # it is used as a sentinel value to check whether cron jobs
                # have been locked for a long time (stuck)
                parse = fields.Datetime.from_string
                oldest = min([parse(job['nextcall']) for job in jobs])
                if datetime.now() - oldest > MAX_FAIL_TIME:
                    odoo.modules.reset_modules_state(db_name)
                else:
                    raise BadModuleState()

            for job in jobs:
                lock_cr = db.cursor()
                lock_cr2 = db.cursor()
                try:
                    # Try to grab an exclusive lock on the job row from within the task transaction
                    # Restrict to the same conditions as for the search since the job may have already
                    # been run by an other thread when cron is running in multi thread
                    lock_cr.execute("""SELECT *
                                           FROM ir_cron
                                           WHERE numbercall != 0
                                              AND active
                                              AND nextcall <= (now() at time zone 'UTC')
                                              AND id=%s
                                           FOR UPDATE NOWAIT""",
                                    (job['id'],), log_exceptions=False)
                    locked_job = lock_cr.fetchone()
                    lock_cr.execute("""UPDATE ir_cron SET running = True
                                           WHERE numbercall != 0
                                              AND active
                                              AND nextcall <= (now() at time zone 'UTC')
                                              AND id=%s""",
                                    (job['id'],), log_exceptions=False)
                    lock_cr.commit()

                    if not locked_job:
                        _logger.debug(
                            "Job `%s` already executed by another process/thread. skipping it",
                            job['cron_name'])
                        continue
                    # Got the lock on the job row, run its code
                    _logger.info('Starting job `%s`.', job['cron_name'])
                    job_cr = db.cursor()
                    try:
                        registry = odoo.registry(db_name)
                        registry[cls._name]._process_job(job_cr, job, lock_cr)
                        lock_cr.execute(
                            """UPDATE ir_cron SET running = False WHERE id=%s""",
                            (job['id'],), log_exceptions=False)
                        lock_cr.commit()
                        _logger.info('Job `%s` done.', job['cron_name'])
                    except Exception:
                        _logger.exception(
                            'Unexpected exception while processing cron job %r',
                            job)
                    finally:
                        job_cr.close()

                except psycopg2.OperationalError as e:
                    if e.pgcode == '55P03':
                        # Class 55: Object not in prerequisite state; 55P03: lock_not_available
                        _logger.debug(
                            'Another process/thread is already busy executing job `%s`, skipping it.',
                            job['cron_name'])
                        continue
                    else:
                        # Unexpected OperationalError
                        raise
                finally:
                    # we're exiting due to an exception while acquiring the lock
                    lock_cr.close()
                    lock_cr2.close()

        finally:
            if hasattr(threading.current_thread(), 'dbname'):
                del threading.current_thread().dbname
