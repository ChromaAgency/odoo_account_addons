from odoo.models import Model
from odoo.exceptions import UserError
from odoo.fields import Float
import logging 

_logger = logging.getLogger(__name__)


class ProductProduct(Model):
    _inherit = "product.product"
    
    def _select_seller(self, partner_id=False, quantity=0.0, date=None, uom_id=False, params=False):
        original_order_company = self.env.context.get('original_order_company', False)
        if original_order_company:
            return super(ProductProduct, self.with_company(original_order_company))._select_seller(partner_id=partner_id, quantity=quantity, date=date, uom_id=uom_id, params=params)
        return super()._select_seller(partner_id=partner_id, quantity=quantity, date=date, uom_id=uom_id, params=params)

    