from odoo.models import Model
from odoo.fields import Many2many

class PurchaseOrder(Model):
    _inherit = "stock.picking.type"

    accounting_company_stock_picking_type_ids = Many2many('stock.picking.type', "stock_picking_type_other_company_stock_pt_rel", "stock_picking_type_id", "other_stock_picking_type_id", string='Tipos de picking contables',copy=False)