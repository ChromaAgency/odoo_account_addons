from odoo.fields import Selection, Float, One2many, Many2one
from odoo.models import Model

class AccountTaxTemplate(Model):
    _inherit = "account.tax.template"

    type_tax_use = Selection(
        selection_add=[
            ('customer', 'Customer Payment'),
            ('supplier', 'Supplier Payment'),
        ],
        ondelete={'customer':"set default",'supplier':"set default"}
    )
    amount_type = Selection(
        selection_add=[
            ('withholding_scale', 'Escala de Retención'),
        ], ondelete={'withholding_scale':"set default"})
    untaxed_amount = Float(string="Monto no sujeto a retención")
    withholding_scale = Many2one('account.withholding.scale', string='Escala de Retención')
