from odoo.models import AbstractModel
from odoo.fields import Many2one,Reference
import logging
_logger = logging.getLogger(__name__)

class AbstractCopy(AbstractModel):
    _name = "abstract.order.accounting"

    accounting_company_id = Many2one('res.company', string='Compañia contable',copy=False)
    original_document_id = Reference( string='Documento original',selection='_selection_accounting_separated_reference_document',copy=False)
    accounting_document_id = Reference(string='Documento contable',selection='_selection_accounting_separated_reference_document',tracking=True,copy=False)

    def _selection_accounting_separated_reference_document(self):
        return [(self._name, self._description)]
    
    def copy_document_to_company(self):
        # self - self allows to have the empty model independently of who is inheriting it.
        copied_documents = self - self
        for rec in self.sudo():
            if rec.accounting_company_id and rec.accounting_company_id != rec.company_id:
                new_record = rec.with_company(rec.accounting_company_id).copy().sudo()
                copied_documents |= new_record
                new_record.with_company(rec.accounting_company_id).company_id = rec.accounting_company_id
                rec.accounting_document_id = "{},{}".format(new_record._name, new_record.id)
                new_record.original_document_id = "{},{}".format(rec._name, rec.id)
        return copied_documents.sudo()