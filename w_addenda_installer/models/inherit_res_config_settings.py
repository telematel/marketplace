# -*- encoding: utf-8 -*-
#
# Module written to Odoo, Open Source Management Solution
#
# Copyright (c) 2021 Telematel - http://www.telematel.com/
# All Rights Reserved.
#
# Developer(s): Nicolás Galindo
#               (ngs@tech.com)
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
#
########################################################################
from odoo import models, fields, api
from ast import literal_eval


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    def _get_default_addendas(self):
        modules_query = ''' 
            SELECT module.id
            FROM ir_module_module AS module
        '''
        addenda = '%' + 'addenda' + '%'
        modules_query +=  '''WHERE module.application is FALSE ''' + '''AND module.name LIKE '%s' '''%(addenda)
        self.env.cr.execute(modules_query)
        modules_ids = self.env.cr.dictfetchall()
        addenda_module_ids = []
        for module_id in modules_ids:
            addenda_module_ids.append(module_id.get('id'))
        addenda_module_ids = self.env['ir.module.module'].search([('id', 'in', addenda_module_ids), ('name', '!=', 'w_addenda_installer')])
        installed_addendas = addenda_module_ids.filtered(lambda a: a.state == 'installed')
        uninstalled_addendas = addenda_module_ids.filtered(lambda a: a.state == 'uninstalled')
        for addenda in installed_addendas:
            addenda.install_addenda = True
        for u_addenda in uninstalled_addendas:
            u_addenda.install_addenda = False
        return addenda_module_ids

    addenda_modules = fields.Many2many('ir.module.module', default=_get_default_addendas)

    def execute(self):
        self.install_uninstall_addendas()
        return super(ResConfigSettings, self).execute()

    def install_uninstall_addendas(self):
        if self.addenda_modules:
            modules_to_install = self.addenda_modules.filtered(lambda m: m.install_addenda == True and m.state!='installed')
            modules_to_uninstall = self.addenda_modules.filtered(lambda m: m.install_addenda == False and m.state!='uninstalled')
            if modules_to_install:
                modules_to_install.button_immediate_install()
            if modules_to_uninstall:
                modules_to_uninstall.button_immediate_uninstall()
