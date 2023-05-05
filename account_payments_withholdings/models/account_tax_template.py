from odoo.fields import Selection
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
