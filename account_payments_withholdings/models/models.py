from odoo import models, fields, api
from odoo.fields import Selection
from odoo.models import Model

class AccountTaxTemplate(Model):
    _inherit = "account.tax.template"

    type_tax_use = Selection(
        selection_add=[
            ('customer', 'Customer Payment'),
            ('supplier', 'Supplier Payment'),
        ],
    )

class AccountTax(Model):
    _inherit = "account.tax"

    type_tax_use = Selection(
        selection_add=[
            ('customer', 'Customer Payment'),
            ('supplier', 'Supplier Payment'),
        ],
    )   

class AccountPayment(models.Model):
    _inherit = "account.payment"

    tax_withholding_id = fields.Many2one(
        'account.tax',
        string='Withholding Tax',
        readonly=True,
        states={'draft': [('readonly', False)]},
    )
    withholding_number = fields.Char(
        string="Número de retención",
        readonly=True,
        states={'draft': [('readonly', False)]},
    )
    withholding_base_amount = fields.Monetary(
        string='Withholding Base Amount',
        readonly=True,
        states={'draft': [('readonly', False)]},
    )

    @api.depends('payment_method_code', 'tax_withholding_id.name')
    def _compute_payment_method_description(self):
        payments = self.filtered(
            lambda x: x.payment_method_code == 'withholding')
        for rec in payments:
            name = rec.tax_withholding_id.name or rec.payment_method_id.name
            rec.payment_method_description = name
        return super(
            AccountPayment,
            (self - payments))._compute_payment_method_description()