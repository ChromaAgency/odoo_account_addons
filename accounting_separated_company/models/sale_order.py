from odoo.models import Model
from odoo.fields import Many2one

class SaleOrder(Model):
    _name = "sale.order"
    _inherit = ["sale.order", "abstract.order.accounting"]

    def action_confirm(self):
        _ = super().action_confirm()
        for rec in self:
            copied_docs = rec.copy_document_to_company()
            copied_docs.action_confirm()
            if copied_docs:
                rec.invoice_status = 'invoiced'
                copied_docs.origin = rec.name  
                copied_docs.client_order_ref = rec.client_order_ref or rec.name
        return _
    
    # TODO: Add relation with invoice and delivery order (Delivery should come from Non accounting company, and invoice from accounting company)