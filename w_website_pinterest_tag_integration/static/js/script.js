odoo.define('w_website_pinterest_tag_integration.pinterest_script', function (require) {
    'use strict';

    var publicWidget = require('web.public.widget');
    var rpc = require('web.rpc');
    var session = require("web.session");
    require('website_sale.website_sale');

    publicWidget.registry.SignUpFormPinterest = publicWidget.Widget.extend({
        selector: '.oe_signup_form',
        events: { 'submit': '_onSubmit', },
        _onSubmit: function (e) {
            // Register signup event
            if(window.pintrk){
                window.sessionStorage.setItem("pinterest_event", "signup");
            }
        },
    });
    //Js add to cart if needed
    publicWidget.registry.WebsiteSale.include({
        _pinterest_add_to_cart: function () {
            if(window.pintrk){
                window.sessionStorage.setItem("pinterest_event", 'add_to_cart');
            }
        },
        _submitForm: function () {
            var result = this._super();
            this._pinterest_add_to_cart();
            return result;
        },
        _changeCartQuantity: function ($input, value, $dom_optional, line_id, productIDs) {
            this._super($input, value, $dom_optional, line_id, productIDs);
            return;
            //TODO: Change Cart Quantity as Add_to_cart
            session.rpc('/pinterest/get_params', {}).then(function (result) {
                if (!result['use_pinterest_tag']) return;
                var email = result['user_email'];
                var tag_id = result['pinterest_tag_key'];

                pintrk('track', 'addtocart', {
                    value: result.website_sale_order.value,
                    order_quantity: result.website_sale_order.order_quantity,
                    currency: result.website_sale_order.currency,
                    order_id: result.website_sale_order.order_id,
                    line_items: result.website_sale_order.line_items,
                });
            });
        },
    });
});
