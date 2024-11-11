from odoo import _
from odoo.models import Model
from ..utils.afip.afip_libro_iva_digital.sicore import SicoreLine, build_and_generate_sicore_txt
import logging
_logger = logging.getLogger(__name__)
from ..utils import float_as_integer_without_separator

class AccountPayment(Model):
    _inherit = 'account.payment'

    def _prepare_arciba_txt_line(self):
        """
        Operation type in payment will always be 2 (Retention)
        Norm will always be 029
        For later implementation the other codes are here:
        https://www.agip.gob.ar/agentes/agentes-de-recaudacion/ib-agentes-recaudacion/aplicativo-arciba/ag-rec-arciba-codigo-de-normas
        date will be payment date

        Get reconciliation line to get an associated document.
        Get document type and number from the associated document. 
        Get document "letter"
        Get document number
        get document date
        get document amount

        get own withholding number

        get partner:
        partner document type (CUIT)
        partner document number
        partnerIB situation
        partnerIB number
        parnter name

        amount other.
        amount iva
        base amount ret-per
        rate
        amount ret-per
        amount ret-per    

        """
        self.ensure_one()
        

    def get_arciba_txt_lines(self):
        lines = []
        for rec in self:
            if not rec.tax_withholding_id:
                continue
            lines.append(rec._prepare_arciba_txt_line())
        return lines
    
    def action_sicore_txt(self):
        return {
            'type': 'ir.actions.act_url',
            'name': "Emitir Txt",
            'url': f'/l10n_ar_withholdings_afip_txt/sicore/{",".join(str(i) for i in self.ids)}',
            'target': 'self',
            'context': self._context, 
        }
    
    def generate_sicore_txt(self):
        lines = []
        for rec in self:
            lines += rec._prepare_afip_sicore()
        return build_and_generate_sicore_txt(lines)
    
    def _prepare_afip_sicore(self):
        """
        """
        document_code = '02' if self.payment_type == 'outbound' else '01'
        document_date = self.date
        document_number = self.sequence_number
        document_amount = self.amount
        tax_code = self.tax_withholding_id.tax_code
        regime_code = self.tax_withholding_id.regime_code
        operation_code = 1 if self.payment_method_line_id.name == 'Retenciones' else 2
        calculation_base = self.withholding_base_amount
        withholding_date = document_date
        condition_code = 1 if self.partner_id.l10n_ar_afip_responsibility_type_id.code == '1' else 2
        withholding_amount = self.amount
        retetion_document_type = self.partner_id.l10n_latam_identification_type_id.l10n_ar_afip_code
        retetion_document_number = str(self.partner_id.vat).replace("-", "").replace(".","")
        original_certificate_number= self.withholding_number

        sicore_line = [
            SicoreLine(
                document_code=document_code,
                document_date=document_date,
                document_number=document_number,
                document_amount=document_amount,
                tax_code=tax_code,
                regime_code =regime_code,
                operation_code=operation_code,
                calculation_base=calculation_base,
                withholding_date =withholding_date,
                condition_code=condition_code,
                withholding_suspended_to_subject=0,
                withholding_amount=withholding_amount,
                exluded_percentage =0,
                publication_date='',
                retention_document_type=retetion_document_type,
                retention_document_number=retetion_document_number,
                original_certificate_number=original_certificate_number,
            )
                                        ]

        return sicore_line