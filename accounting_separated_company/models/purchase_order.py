from odoo.models import Model
from odoo.exceptions import UserError
from odoo.fields import Float, Char
import logging 
from odoo.api import depends

_logger = logging.getLogger(__name__)


class PurchaseOrderLine(Model):
    _inherit = "purchase.order.line"

    @depends('product_qty', 'product_uom', 'company_id')
    def _compute_price_unit_and_date_planned_and_name(self):
        if self.order_id.original_document_id:
            return super(PurchaseOrderLine, self.with_context(original_order_company=self.order_id.original_document_id.company_id.id))._compute_price_unit_and_date_planned_and_name()
        return super(PurchaseOrderLine, self)._compute_price_unit_and_date_planned_and_name()

class PurchaseOrder(Model):
    _name = "purchase.order"
    _inherit = ["purchase.order", "abstract.order.accounting"]

    copied_purchase_order_name = Char(string="Pedidos de compra copiados")

    def button_confirm(self):
        _ = super().button_confirm()
        for rec in self:
            if not rec.accounting_company_id or rec.accounting_company_id == rec.company_id:
                continue
            copied_docs = rec.copy_document_to_company()
            # picking_type_id = copied_docs.picking_type_id.accounting_company_stock_picking_type_ids \
            #                             .filtered(lambda x: x.company_id.id == rec.accounting_company_id.id)
            # if not picking_type_id:
            #     raise UserError("No se ha encontrado un tipo de picking contable para la compañia %s, verifique la configuración y vuelva a intentarlo" % rec.accounting_company_id.name)
            # copied_docs.picking_type_id = picking_type_id[0].id
            copied_docs.button_confirm()
            if copied_docs:
                rec.invoice_status = 'invoiced'
                copied_docs.origin = rec.name  
                copied_docs.partner_ref = rec.partner_ref or rec.name
        return _


    def button_cancel(self):
        _ = super().button_cancel()
        related_purchase_order = []
        for rec in self:
            related_purchase_order.append(rec.copied_purchase_order_name)        
        orders_to_cancel = self.env['purchase.order'].search([('name','in',related_purchase_order)])
        for order in orders_to_cancel:
            order.button_cancel()
        return _

    # TODO: Add relation with invoice and reception order (reception should come from Non accounting company, and invoice from accounting company)
    