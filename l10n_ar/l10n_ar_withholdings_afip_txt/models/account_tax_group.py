from odoo import models, fields

class AccountTaxGroup(models.Model):
    _inherit = 'account.tax.group'

    tax_type = fields.Selection([('national','Impuesto nacional'),('perception','Percepción'),('vat','IVA'),('iibb','IIBB'),('city','IVA de ciudad')], string="Tipo de impuesto")
