from odoo import models, fields

class AccountTax(models.Model):
    _inherit = 'account.tax'

    is_national_tax = fields.Boolean(string="Es impuesto nacional")
    is_perception_tax = fields.Boolean(string="Es percepción")
    is_vat_tax = fields.Boolean(string="Es IVA")
    is_iibb_tax = fields.Boolean(string="Es IIBB")
    is_city_tax = fields.Boolean(string="Es IVA de ciudad")
