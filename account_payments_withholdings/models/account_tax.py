from odoo.fields import Selection, Float
from odoo.models import Model

class AccountTax(Model):
    _inherit = "account.tax"

    type_tax_use = Selection(
        selection_add=[
            ('customer', 'Customer Payment'),
            ('supplier', 'Supplier Payment'),
        ],
        ondelete={'customer':"set default",'supplier':"set default"}
    )
    untaxed_amount = Float(string="Monto no sujeto a retención")

