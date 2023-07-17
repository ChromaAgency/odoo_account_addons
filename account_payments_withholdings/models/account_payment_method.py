from odoo.models import Model
from odoo.api import model

class AccountPayment(Model):
    _inherit = "account.payment.method"
    
    @model
    def _get_payment_method_information(self):
        vals = super()._get_payment_method_information()
        vals.update({  'withholding': {'mode': 'multi', 'domain': [('type', 'in', ('bank', 'cash'))]}})
        return vals

