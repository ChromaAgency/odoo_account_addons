from dataclasses import dataclass, field, asdict
from typing import Dict, List
from datetime import date, datetime
from ...column_width_generator import FixedColumnWidthCSVGenerator
import logging
_logger = logging.getLogger(__name__)
alicuotas_cols = {
    "document_code":2,
    "document_date":10,
    "document_number":14,
    "document_amount":16,
    "tax_code":3,
    "regime_code":3,
    "operation_code":1,
    "calculation_base":14,
    "withholding_date":10,
    "condition_code":2,
    "withholding_suspended_to_subject":1,
    "withholding_amount":14,
    "exluded_percentage":6,
    "publication_date":10,
    "retention_document_type":2, #CUIT
    "retention_document_number":20, #NroDeCuit
    "original_certificate_number":14,
    

}

def generate_afip_txt_generator():
    afip_txt_generator = FixedColumnWidthCSVGenerator()
    aligns = {
        float:">",
        int:">",
        str:"<",
    }
    fills = {
        str:" ",
        float:"0",
        int:"0",
    }

    formats = {
        float:".2f",
        int:"",
        str:"",
        date:"%Y%m%d",
    }

    post_process_fn = {
        float:lambda x: x.replace(".", ",")
    }
    for name, t in vars(SicoreLine)['__annotations__'].items():
        afip_txt_generator.add_column(formats.get(t, ""), aligns.get(t, ""), fills.get(t, ""), alicuotas_cols[name], post_process_fn.get(t, lambda x: x))
    return afip_txt_generator
        
@dataclass
class SicoreLine:

    document_code: int
    document_date: date
    document_number: int
    document_amount: float
    tax_code: int
    regime_code : int
    operation_code: int
    calculation_base: float
    withholding_date : date
    condition_code: int
    withholding_suspended_to_subject: int
    withholding_amount: float
    exluded_percentage : float
    publication_date: date
    retention_document_type: str
    retention_document_number: int
    original_certificate_number: int



    def add_line_to_generator(self, generator:FixedColumnWidthCSVGenerator):
        retper_date = self.retper_date
        doc_date = self.doc_date
        generator.add_line_with_args(self.op_type, self.norm, retper_date, self.doc_type, self.doc_letter, self.doc_number, doc_date, self.doc_amount, self.ret_number, self.afip_document_type, self.afip_document_number, self.ib_type, self.ib_number, self.iva_type, self.name, self.amount_other, self.amount_iva, self.base_amount_for_tax, self.tax_rate, self.tax_amount, self.tax_retention)

def build_and_generate_sicore_txt(lines:List[SicoreLine]):         
    arciba_txt_generator = generate_afip_txt_generator()
    for l in lines:
        ldict = asdict(l)
        vendor_nif = ldict['vendor_nif']
        emisor_vat = ldict['emisor_vat']
        if vendor_nif:
            ldict['vendor_nif'] = vendor_nif.replace("-", "").replace(".","")
        if emisor_vat:
            ldict['emisor_vat'] = int(str(emisor_vat).replace("-", "").replace(".", ""))
        arciba_txt_generator.add_line_with_args(*ldict.values())
    return arciba_txt_generator.build()