from odoo import fields, models


class Website(models.Model):
    _inherit = "website"

    use_pinterest_tag = fields.Boolean("Use Pinterest Tag",
                                       help='Use Pinterest Tag tracking system')
    pinterest_tag_key = fields.Char("Pinterest Tag ID")
    # reg_page_visit = fields.Boolean("Page Visit", help='Pinterest register user visit in all webpages for this site', default=True)
    # reg_signup = fields.Boolean("Signup", help='Pinterest register users signup', default=True)
    # reg_checkout = fields.Boolean("Checkout", help='Pinterest register product checkout', default=True)
