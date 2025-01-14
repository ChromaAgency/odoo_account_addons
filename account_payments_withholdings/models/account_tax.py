from odoo.fields import Selection, Float, One2many, Many2one
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
    amount_type = Selection(
        selection_add=[
            ('withholding_scale', 'Escala de Retención'),
        ], ondelete={'withholding_scale':"set default"})
    
    untaxed_amount = Float(string="Monto no sujeto a retención")
    withholding_scale = Many2one('account.withholding.scale', string='Escala de Retención')

    def get_withholding_amount(self, amount):
        """
        This method is used to obtain the withholding amount, it returns a base amount to be withhold, and the percentage
        returns base_amount, amount
        """
        if self.amount_type == 'withholding_scale':
            return self.withholding_scale.obtain_withholding_scale(amount)
        return 0, self.amount / 100, 0