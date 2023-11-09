from odoo import _
from odoo.models import Model

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