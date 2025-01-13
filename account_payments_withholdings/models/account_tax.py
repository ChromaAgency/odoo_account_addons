from odoo.fields import Selection, Float, One2many, Many2one
from odoo.models import Model

class AccountTax(Model):
    _inherit = "account.tax"

    type_tax_use = Selection(
        selection_add=[
            ('customer', 'Customer Payment'),
            ('supplier', 'Supplier Payment'),
            ('withholding_scale', 'Escala de Retención'),
        ],
        ondelete={'customer':"set default",'supplier':"set default", 'withholding_scale':"set default"}
    )
    untaxed_amount = Float(string="Monto no sujeto a retención")
    withholding_scale = Many2one('account.withholding.scale', string='Escala de Retención')

