# -*- encoding: utf-8 -*-
#
# Module written to Odoo, Open Source Management Solution
#
# Copyright (c) 2017 Telematel - http://www.telematel.com/
# All Rights Reserved.
#
# Developer(s): Alan Guzmán
#               (age@wedoo.tech)
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
from odoo import api, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.multi
    def action_invoice_create(self, grouped=False, final=False):
        res = super(SaleOrder, self).action_invoice_create(
            grouped=grouped, final=final)
        invoice_ids = []
        sale_ids = []
        if self.opportunity_id:
            sale_ids = self.env['sale.order'].search([
                ('opportunity_id', '=', self.opportunity_id.id)])
            for sale in sale_ids:
                invoice_ids.append(sale.invoice_ids)
            inv_ids = [inv.id for inv in invoice_ids]
            inv_ids = [inv for inv in inv_ids if type(inv) is int]
            invoices = inv_ids + res
            sql = """SELECT MAX(amount_total) FROM account_invoice
            WHERE id IN ({})""".format(",".join([str(
                inv) for inv in invoices]))
            self._cr.execute(sql)
            if self._cr.rowcount:
                lead_id = self.opportunity_id
                dict_amount = self._cr.dictfetchone()
                amount = dict_amount.get('max', False)
                lead_id.planned_revenue = amount
        return res
