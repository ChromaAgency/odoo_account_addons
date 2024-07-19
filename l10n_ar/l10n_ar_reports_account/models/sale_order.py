from odoo.models import Model
from odoo.fields import Many2one

class SaleOrder(Model):
    _inherit = "sale.order"

    def _prepare_invoice(self):
        invoice_vals = super(SaleOrder, self)._prepare_invoice()

        invoice_vals.update({
        'stock_picking_ids':self.picking_ids.ids,
        })
        return invoice_vals