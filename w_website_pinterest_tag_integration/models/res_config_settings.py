from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    use_pinterest_tag = fields.Boolean(related="website_id.use_pinterest_tag", readonly=False)
    pinterest_tag_key = fields.Char(related="website_id.pinterest_tag_key", readonly=False)
    # reg_page_visit = fields.Boolean(related="website_id.reg_page_visit", readonly=False)
    # reg_signup = fields.Boolean(related="website_id.reg_signup", readonly=False)
    # reg_checkout = fields.Boolean(related="website_id.reg_checkout", readonly=False)
