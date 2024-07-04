from odoo.models import Model
from odoo.fields import Many2one, Char
from odoo.api import depends, onchange
import logging 
_logger = logging.getLogger(__name__)

class SaleOrder(Model):
    _name = "sale.order"
    _inherit = ["sale.order", "abstract.order.accounting"]

    copied_sale_order_name = Char(string="Pedidos de venta copiados", store=True)

    def action_confirm(self):
        _ = super().action_confirm()
        for rec in self:
            copied_docs = rec.copy_document_to_company()
            copied_docs.action_confirm()
            if copied_docs:
                rec.invoice_status = 'invoiced'
                copied_docs.origin = rec.name  
                copied_docs.client_order_ref = rec.client_order_ref or rec.name
                rec.copied_sale_order_name = copied_docs.name
        return _
    
    # TODO: Add relation with invoice and delivery order (Delivery should come from Non accounting company, and invoice from accounting company)

    def action_cancel(self):
        _ = super().action_cancel()
        related_sale_orders = []
        for rec in self:
            related_sale_orders.append(rec.copied_sale_order_name)        
        orders_to_cancel = self.env['sale.order'].search([('name','in',related_sale_orders)])
        for order in orders_to_cancel:
            order.action_cancel()
        return _
    

    def write(self, vals):
        result = super().write(vals)
        if 'accounting_company_id' in vals:
            if self.accounting_company_id and self.state in ['sale','done'] and not self.copied_sale_order_name:
                copied_docs = self.copy_document_to_company()
                copied_docs.action_confirm()
                if copied_docs:
                    self.invoice_status = 'invoiced'
                    copied_docs.origin = self.name  
                    copied_docs.client_order_ref = self.client_order_ref or self.name
                    self.copied_sale_order_name = copied_docs.name
        return result