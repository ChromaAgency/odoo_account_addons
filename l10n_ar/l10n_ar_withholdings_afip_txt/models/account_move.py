from ..utils import float_as_integer_without_separator
from ..utils.afip.afip_libro_iva_digital.alicuotas_ventas import AlicuotasVentasLine, build_and_generate_ventas_alicuotas_txt
from ..utils.afip.afip_libro_iva_digital.comprobantes_ventas import VentasComprobantesLine, build_and_generate_ventas_comprobantes_txt
from odoo import _
from odoo.models import Model
import logging
_logger = logging.getLogger(__name__)
class AccountMove(Model):
    _inherit = 'account.move'

    def _prepare_afip_ventas_alicuotas(self):
        """
        Tabla Alicuotas
        CÓDIGO DESCRIPCIÓN
        0003 0,00 %
        0004 10,50 %
        0005 21,00 %
        0006 27,00 %
        0008 5,00 %
        0009 2,50 %
        """
        alicuotas = {
            21:5,
            10.5:4,
            0:3,
            27:6,
            5:8,
            2.5:9,
        }
        self.ensure_one()
        # TODO make it safer
        lines = self.invoice_line_ids.filtered(lambda x: x.tax_ids and 'IVA' in x.tax_ids.tax_group_id.name )
        lines_alicuotas = lines.tax_ids.mapped("amount")
        return [
            AlicuotasVentasLine(doc_type=2, 
                                pos=int(self.journal_id.code), 
                                doc_number=self.sequence_number, 
                                net_amount=float_as_integer_without_separator(sum(lines.mapped("price_subtotal"))), 
                                iva_rate=alicuotas[alicuota], 
                                iva_amount=float_as_integer_without_separator(sum(lines.mapped("price_subtotal"))*(alicuota/100))) for alicuota in lines_alicuotas]

    def _prepare_afip_ventas_comprobantes(self):
        """
        Tipos de comprobantes (Probably abstract to minimize overhead on this class.)
            Are the same as odoo code

        Código de Operación
        Código Descripción COMPRAS Descripción VENTAS
        A No Alcanzado No Alcanzado
        (espacio) o
        0 (cero) No corresponde No corresponde
        C Operac. Canje Operac. Canje
        D Devol. IVA Turistas Extr. Devol. IVA Turistas Extr.
        E Operaciones Exentas Operaciones Exentas
        N No gravado No gravado
        T Reintegro Decreto 1043/2016 Reintegro Decreto 1043/2016
        X Importación del Exterior Exportación al Exterior
        Z Importación de Zona Franca Exportación a Zona Franca
        """
        doc_code = self.partner_id.l10n_latam_identification_type_id.l10n_ar_afip_code
        nif = self.partner_id.vat   
        doct_type_id = self.l10n_latam_document_type_id_code
        lines = self.invoice_line_ids.filtered(lambda x: x.tax_ids and 'IVA' in x.tax_ids.tax_group_id.name )
        lines_alicuotas = lines.tax_ids.mapped("amount")
        amount_of_rates = len(lines_alicuotas)
        amount_total = float_as_integer_without_separator(self.amount_total)
        amount_total = float_as_integer_without_separator(self.amount_total)
        excluded_tax_lines = self.invoice_line_ids - lines
        amount_total_of_excluded_lines = float_as_integer_without_separator(sum(excluded_tax_lines.mapped("price_total")))
        amount_untaxed_of_excluded_lines = float_as_integer_without_separator(sum(excluded_tax_lines.mapped("price_subtotal")))
        return [
            VentasComprobantesLine(doc_date=self.invoice_date,doc_type=doct_type_id, pos=int(self.journal_id.code), doc_number=self.sequence_number,
                                       doc_number_to=self.sequence_number, buyer_doc_code=doc_code, buyer_nif=nif, buyer_full_name=self.partner_id.display_name, 
                                       total_amount=amount_total, other_amount=amount_total_of_excluded_lines, non_categorized_perception=0, 
                                       tax_excluded_operation_amount=amount_untaxed_of_excluded_lines, national_perceptions_amount=0, iibb_perceptions_amount=0, city_perceptions_amount=0,internal_taxes_amount=0,
                                       currency_code=self.currency_id.l10n_ar_afip_code, exchange_rate=float_as_integer_without_separator(self.l10n_ar_currency_rate, 6) , IVA_rates_amount=amount_of_rates, op_code=0, other_taxes=0,
                                       due_date=self.invoice_date_due, )
                                        ]        

    def generate_ventas_alicuotas_txt(self):
        lines = []
        for rec in self:
            lines += rec._prepare_afip_ventas_alicuotas()
        return build_and_generate_ventas_alicuotas_txt(lines)

    
    def generate_ventas_comprobantes_txt(self):
        lines = []
        for rec in self:
            lines += rec._prepare_afip_ventas_comprobantes()
        return build_and_generate_ventas_comprobantes_txt(lines)

    def action_ventas_comprobantes_txt(self):
        return {
            'type': 'ir.actions.act_url',
            'name': "Emitir Txt",
            'url': f'/l10n_ar_withholdings_afip_txt/comprobante_venta/{",".join(str(i) for i in self.ids)}',
            'target': 'self',
            'context': self._context, 
        }
    
    def action_ventas_alicuotas_txt(self):
        return {
            'type': 'ir.actions.act_url',
            'name': "Emitir Txt",
            'url': f'/l10n_ar_withholdings_afip_txt/alicuotas_venta/{",".join(str(i) for i in self.ids)}',
            'target': 'self',
            'context': self._context, 
        }