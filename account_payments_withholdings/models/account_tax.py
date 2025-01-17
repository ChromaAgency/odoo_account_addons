from odoo.fields import Boolean, Selection, Float, One2many, Many2one
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
            ('by_group', 'Por grupos'),
        ], ondelete={'by_group':'set default', 'withholding_scale':"set default"})
    
    untaxed_amount = Float(string="Monto no sujeto a retención")
    withholding_scale = Many2one('account.withholding.scale', string='Escala de Retención')
    withholding_group = Many2one('account.withholding.group', string='Grupos de Retención')
    take_out_untaxed_amount = Boolean(string="Descontar monto no sujeto a retención", default=True)

    def get_withholding_amount(self, amount, partner):
        """
        This method is used to obtain the withholding amount, it returns a base amount to be withhold, and the percentage
        returns base_amount, amount
        """
        if self.amount_type == 'by_group':
            return 0, self.withholding_group.obtain_withholding_group_amount(partner), 0
        if self.amount_type == 'withholding_scale':
            return self.withholding_scale.obtain_withholding_scale(amount)
        return 0, self.amount / 100, 0