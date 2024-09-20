from odoo.models import AbstractModel
from odoo.fields import Many2one,Reference
import logging
from odoo.exceptions import UserError
_logger = logging.getLogger(__name__)

class AbstractCopy(AbstractModel):
    _name = "abstract.order.accounting"

    accounting_company_id = Many2one('res.company', string='Compañia contable',copy=False)
    original_document_id = Reference( string='Documento original',selection='_selection_accounting_separated_reference_document',copy=False)
    accounting_document_id = Reference(string='Documento contable',selection='_selection_accounting_separated_reference_document',copy=False)

    def _selection_accounting_separated_reference_document(self):
        return [(self._name, self._description)]
    
    def copy_document_to_company(self):
        _logger.info('inside copy document')
        copied_documents = self - self
        for rec in self.sudo():
            if rec.accounting_company_id and rec.accounting_company_id != rec.company_id:
                new_order_lines = []
                for line in rec.order_line:
                    new_taxes = self.env['account.tax'].search([
                        ('name', 'in', line.tax_id.mapped('name')),
                        ('company_id', '=', rec.accounting_company_id.id)
                    ])
                    
                    if not new_taxes:
                        raise UserError(f"No se encontraron impuestos para la compañía destino en la orden {self.name}.")

                    copied_line = line.with_company(rec.accounting_company_id).copy({
                        'tax_id': new_taxes.ids
                    }).sudo()
                    new_order_lines.append((4, copied_line.id))
                
                new_record = rec.with_company(rec.accounting_company_id).copy({
                    'company_id': rec.accounting_company_id.id,
                    'order_line': new_order_lines 
                }).sudo()
                
                copied_documents |= new_record
                rec.accounting_document_id = "{},{}".format(new_record._name, new_record.id)
                new_record.original_document_id = "{},{}".format(rec._name, rec.id)
        
        return copied_documents.sudo()