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
    "dispatch_number":16,
    "vendor_doc_code":2,
    "vendor_nif":20,
    "vendor_full_name":30,
    "total_amount":15,
    "other_amount":15,
    "tax_excluded_operation_amount":15,
    "perceptions_or_payment_IVA_amount":15,
    "another_national_perceptions_amount":15,
    "iibb_perceptions_amount":15,
    "city_perceptions_amount":15,
    "internal_taxes_amount":15,
    "currency_code":3,
    "exchange_rate":10,
    "IVA_rates_amount":1,
    "op_code":1,
    "computable_fiscal_credit":15,
    "other_taxes":15,
    "emisor_vat":11,
    "emisor_denomination":30,
    "vat_commission":15,
    

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
    for name, t in vars(ComprasComprobantesLine)['__annotations__'].items():
        afip_txt_generator.add_column(formats.get(t, ""), aligns.get(t, ""), fills.get(t, ""), alicuotas_cols[name], post_process_fn.get(t, lambda x: x))
    return afip_txt_generator
        
@dataclass
class ComprasComprobantesLine:
    """
    Spec according to Libro IVA digital
    Source 2023: https://www.afip.gob.ar/libro-iva-digital/documentos/libro-iva-digital-diseno-registros.pdf
    """
    doc_date:date
    doc_type:int
    pos:int
    doc_number:int
    dispatch_number:str
    vendor_doc_code:int
    vendor_nif:str
    vendor_full_name:str
    total_amount:int
    other_amount:int
    tax_excluded_operation_amount:int
    perceptions_or_payment_IVA_amount:int 
    another_national_perceptions_amount:int 
    iibb_perceptions_amount:int 
    city_perceptions_amount:int 
    internal_taxes_amount:int
    currency_code:str
    exchange_rate:int
    IVA_rates_amount:int
    op_code:str
    computable_fiscal_credit:int 
    other_taxes:int
    emisor_vat:int 
    emisor_denomination:str 
    #TODO adaptar a factura de liquido producto
    vat_commission:int 


    def add_line_to_generator(self, generator:FixedColumnWidthCSVGenerator):
        retper_date = self.retper_date
        doc_date = self.doc_date
        generator.add_line_with_args(self.op_type, self.norm, retper_date, self.doc_type, self.doc_letter, self.doc_number, doc_date, self.doc_amount, self.ret_number, self.afip_document_type, self.afip_document_number, self.ib_type, self.ib_number, self.iva_type, self.name, self.amount_other, self.amount_iva, self.base_amount_for_tax, self.tax_rate, self.tax_amount, self.tax_retention)

def build_and_generate_compras_comprobantes_txt(lines:List[ComprasComprobantesLine]):         
    arciba_txt_generator = generate_afip_txt_generator()
    for l in lines:
        ldict = asdict(l)
        ldict['vendor_nif'] = ldict['vendor_nif'].replace("-", "")
        ldict['emisor_vat'] = int(str(ldict['emisor_vat']).replace("-", ""))
        arciba_txt_generator.add_line_with_args(*ldict.values())
    return arciba_txt_generator.build()