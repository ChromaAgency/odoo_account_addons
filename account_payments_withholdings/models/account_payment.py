from odoo.fields import Many2one, Char, Monetary
from odoo.models import Model
from odoo.api import depends

class AccountPayment(Model):
    _inherit = "account.payment"

    tax_withholding_id = Many2one(
        'account.tax',
        string='Withholding Tax',
        readonly=True,
        states={'draft': [('readonly', False)]},
    )
    withholding_number = Char(
        string="Número de retención",
        readonly=True,
        states={'draft': [('readonly', False)]},
    )
    withholding_base_amount = Monetary(
        string='Withholding Base Amount',
        readonly=True,
        states={'draft': [('readonly', False)]},
    )

    @depends('payment_method_code', 'tax_withholding_id.name')
    def _compute_payment_method_description(self):
        payments = self.filtered(
            lambda x: x.payment_method_code == 'withholding')
        for rec in payments:
            name = rec.tax_withholding_id.name or rec.payment_method_id.name
            rec.payment_method_description = name
        return super(
            AccountPayment,
            (self - payments))._compute_payment_method_description()
    
