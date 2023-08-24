from odoo.models import Model
from odoo.exceptions import UserError
import logging 

_logger = logging.getLogger(__name__)

class PurchaseOrder(Model):
    _name = "purchase.order"
    _inherit = ["purchase.order", "abstract.order.accounting"]

    def button_confirm(self):
        _ = super().button_confirm()
        for rec in self:
            if not rec.accounting_company_id:
                continue
            copied_docs = rec.copy_document_to_company()
            picking_type_id = copied_docs.picking_type_id.accounting_company_stock_picking_type_ids \
                                        .filtered(lambda x: x.company_id.id == rec.accounting_company_id.id)
            if not picking_type_id:
                raise UserError("No se ha encontrado un tipo de picking contable para la compañia %s, verifique la configuración y vuelva a intentarlo" % rec.accounting_company_id.name)
            copied_docs.picking_type_id = picking_type_id[0].id
            copied_docs.button_confirm()
            if copied_docs:
                rec.invoice_status = 'invoiced'
                copied_docs.origin = rec.name  
                copied_docs.partner_ref = rec.partner_ref or rec.name
        return _


    # TODO: Add relation with invoice and reception order (reception should come from Non accounting company, and invoice from accounting company)
    