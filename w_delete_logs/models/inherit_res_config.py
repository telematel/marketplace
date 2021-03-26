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
from odoo import api, fields, models
from odoo.tools.safe_eval import safe_eval
import datetime
from dateutil.relativedelta import relativedelta

TIMES = [
    ('one_week', 'One Week'),
    ('fifteen_days', 'Fifteen Days'),
    ('one_month', 'One Month'),
    ('three_month', 'Three Months'),
    ('six_month', 'Six Months'),
    ('one_year', 'One Year'),
]


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    model_ids = fields.Many2many(
        'ir.model',
        'ir_model_config_rel',
        string='Models'
    )
    times = fields.Selection(
        TIMES,
        string="Times",
        default="three_month"
    )

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        Config = self.env['ir.config_parameter'].sudo()
        model_log_ids = safe_eval(Config.get_param("model_logs", "[]"))
        model_log_real_ids = self.sudo().env["ir.model"].search(
            [("id", "in", model_log_ids)])
        times = Config.get_param("times", "three_month")
        values = {
            "model_ids": [(6, 0, model_log_real_ids.ids)],
            "times": times,
        }
        res.update(values)
        return res

    def set_values(self):
        super(ResConfigSettings, self).set_values()
        Config = self.env['ir.config_parameter'].sudo()
        Config.set_param("model_logs", self.model_ids.ids)
        Config.set_param("times", self.times)

    def deleting_model_logs(self):
        Config = self.env['ir.config_parameter'].sudo()
        model_log_ids = safe_eval(Config.get_param("model_logs", "[]"))
        model_log_real_ids = self.sudo().env["ir.model"].search(
            [("id", "in", model_log_ids)])
        times = Config.get_param("times", "three_month")
        for model in model_log_real_ids:
            now = datetime.datetime.utcnow()
            if times == 'one_week':
                date = now - datetime.timedelta(weeks=1)
            elif times == 'fifteen_days':
                date = now - datetime.timedelta(days=15)
            elif times == 'one_month':
                date = now - relativedelta(months=1)
            elif times == 'three_month':
                date = now - relativedelta(months=3)
            elif times == 'six_month':
                date = now - relativedelta(months=6)
            else:
                date = now - relativedelta(years=1)
            domain = [
                ('create_date', '<', date)
            ]
            records = self.env[model.model].sudo().search(domain)
            records.sudo().unlink()
