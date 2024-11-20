from odoo import models, fields

class AccountTax(models.Model):
    _inherit = 'account.tax'

    tax_code = fields.Char(string="Código de impuesto")
    regime_code = fields.Char(string="Código de regimen")