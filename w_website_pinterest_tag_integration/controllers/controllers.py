# -*- coding: utf-8 -*-

from odoo import http
from odoo.http import request
import logging

_logger = logging.getLogger(__name__)


class PinterestController(http.Controller):

    @http.route(['/pinterest/get_params'], type='json', auth="user", website='true')
    def pinterest_get_params(self, **kwargs):
        website_sale_order = request.website.sale_get_order()

        return {
            'use_pinterest_tag': request.website.use_pinterest_tag,
            'pinterest_tag_key': request.website.pinterest_tag_key,
            'user_id': request.env.user.id,
            'user_email': request.env.user.email,
            'company_id': request.website.company_id.id,
            'website_sale_order': {
                'value': website_sale_order.amount_total,
                'order_quantity': website_sale_order.cart_quantity,
                'currency': website_sale_order.currency_id.name,
                'order_id': website_sale_order.name,
                'line_items': [{
                    'product_name': line.product_id.name,
                    'product_category': line.product_id.categ_id.name,
                    'product_id': line.product_id.default_code or line.product_id.id,
                    'product_price': line.product_id.lst_price,
                    'product_quantity': line.product_uom_qty,
                } for line in website_sale_order.order_line]
            }
        }
