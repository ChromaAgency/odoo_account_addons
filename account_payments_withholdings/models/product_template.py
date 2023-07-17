from odoo.fields import Many2many
from odoo.models import Model

class ProductTemplate(Model):
    _inherit = "product.template"

    product_withholding_ids = Many2many('account.tax', 'withholding_product_product_account_tax_rel', 'product_product_id', 'account_tax_id', string='Retenciones aplicables')


