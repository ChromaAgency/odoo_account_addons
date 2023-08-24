from odoo.models import AbstractModel
from odoo.fields import Many2one

class AbstractCopy(AbstractModel):
    _name = "abstract.order.accounting"

    accounting_company_id = Many2one('res.company', string='Compañia contable',copy=False)

    def copy_document_to_company(self):
        # self - self allows to have the empty model independently of who is inheriting it.
        copied_documents = self - self
        for rec in self.sudo():
            if rec.accounting_company_id:
                new_record = rec.with_company(rec.accounting_company_id).copy().sudo()
                copied_documents |= new_record
                new_record.with_company(rec.accounting_company_id).company_id = rec.accounting_company_id
        return copied_documents.sudo()