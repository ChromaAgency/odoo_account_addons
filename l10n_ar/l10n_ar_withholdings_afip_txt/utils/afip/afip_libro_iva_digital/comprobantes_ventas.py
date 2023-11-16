from dataclasses import dataclass, field, asdict
from typing import Dict, List
from datetime import date, datetime
from ...column_width_generator import FixedColumnWidthCSVGenerator
import logging
_logger = logging.getLogger(__name__)
alicuotas_cols = {
    "doc_date":8,
    "doc_type":3,
    "pos":5,
    "doc_number":20,
    "doc_number_to":20,
    "buyer_doc_code":2,
    "buyer_nif":20,
    "buyer_full_name":30,
    "total_amount":15,
    "other_amount":15,
    "non_categorized_perception":15,
    "tax_excluded_operation_amount":15,
    "national_perceptions_amount":15,
    "iibb_perceptions_amount":15,
    "city_perceptions_amount":15,
    "internal_taxes_amount":15,
    "currency_code":3,
    "exchange_rate":10,
    "IVA_rates_amount":1,
    "op_code":1,
    "other_taxes":15,
    "due_date":8,
    

}

def generate_arciba_txt_generator():
    arciba_txt_generator = FixedColumnWidthCSVGenerator()
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
    for name, t in vars(VentasComprobantesLine)['__annotations__'].items():
        arciba_txt_generator.add_column(formats.get(t, ""), aligns.get(t, ""), fills.get(t, ""), alicuotas_cols[name], post_process_fn.get(t, lambda x: x))
    return arciba_txt_generator
        
@dataclass
class VentasComprobantesLine:
    """
    Spec according to Libro IVA digital
    Source 2023: https://www.afip.gob.ar/libro-iva-digital/documentos/libro-iva-digital-diseno-registros.pdf
    """
    doc_date:date
    doc_type:int
    pos:int
    doc_number:int
    doc_number_to:int
    buyer_doc_code:int
    buyer_nif:int
    buyer_full_name:str
    total_amount:int
    other_amount:int
    non_categorized_perception:int
    tax_excluded_operation_amount:int
    national_perceptions_amount:int
    iibb_perceptions_amount:int
    city_perceptions_amount:int
    internal_taxes_amount:int
    currency_code:str
    exchange_rate:int
    IVA_rates_amount:int
    op_code:str
    other_taxes:int
    due_date:date


    def add_line_to_generator(self, generator:FixedColumnWidthCSVGenerator):
        retper_date = self.retper_date
        doc_date = self.doc_date
        generator.add_line_with_args(self.op_type, self.norm, retper_date, self.doc_type, self.doc_letter, self.doc_number, doc_date, self.doc_amount, self.ret_number, self.afip_document_type, self.afip_document_number, self.ib_type, self.ib_number, self.iva_type, self.name, self.amount_other, self.amount_iva, self.base_amount_for_tax, self.tax_rate, self.tax_amount, self.tax_retention)

def build_and_generate_ventas_comprobantes_txt(lines:List[VentasComprobantesLine]):         
    arciba_txt_generator = generate_arciba_txt_generator()
    for l in lines:
        ldict = asdict(l)
        ldict['buyer_nif'] = ldict['buyer_nif'].replace("-", "")
        arciba_txt_generator.add_line_with_args(*ldict.values())
    return arciba_txt_generator.build()