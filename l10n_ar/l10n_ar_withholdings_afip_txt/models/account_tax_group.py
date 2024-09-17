from odoo import models, fields

class AccountTaxGroup(models.Model):
    _inherit = 'account.tax.group'

    tax_type = fields.Selection([('national','Impuesto nacional'),('perception','Percepción'),('vat','IVA'),('iibb','IIBB'),('city','Impuesto municipal')], string="Tipo de impuesto")
