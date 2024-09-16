from dataclasses import dataclass, field, asdict
from typing import Dict, List
from datetime import date
from ...column_width_generator import FixedColumnWidthCSVGenerator

alicuotas_cols = {
    "doc_type":3,
    "pos":5,
    "doc_number":20,
    "vendor_document_code":2,
    "vendor_document_number":20,
    "net_amount":15,
    "iva_rate":4,
    "iva_amount":15,

}

def generate_afip_text_generator():
    afip_txt_generator = FixedColumnWidthCSVGenerator()
    aligns = {
        float:"<",
        str:">",
        int:">",
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
        date:"%d%m%Y",
    }

    post_process_fn = {
        float:lambda x: x.replace(".", ",")
    }
    for name, t in vars(AlicuotasComprasLine)['__annotations__'].items():
        afip_txt_generator.add_column(formats.get(t, ""), aligns.get(t, ""), fills.get(t, ""), alicuotas_cols[name], post_process_fn.get(t, lambda x: x))
    return afip_txt_generator
        
@dataclass
class AlicuotasComprasLine:
    """
    Spec according to Libro IVA digital
    Source 2023: https://www.afip.gob.ar/libro-iva-digital/documentos/libro-iva-digital-diseno-registros.pdf
    """
    doc_type:int
    pos:int
    doc_number:int
    vendor_document_code:int
    vendor_document_number:int
    net_amount:int
    iva_rate:int
    iva_amount:int


    def add_line_to_generator(self, generator:FixedColumnWidthCSVGenerator):
        retper_date = self.retper_date
        doc_date = self.doc_date
        generator.add_line_with_args(self.op_type, self.norm, retper_date, self.doc_type, self.doc_letter, self.doc_number, doc_date, self.doc_amount, self.ret_number, self.afip_document_type, self.afip_document_number, self.ib_type, self.ib_number, self.iva_type, self.name, self.amount_other, self.amount_iva, self.base_amount_for_tax, self.tax_rate, self.tax_amount, self.tax_retention)

def build_and_generate_compras_alicuotas_txt(lines:List[AlicuotasComprasLine]):         
    arciba_txt_generator = generate_afip_text_generator()
    for l in lines:
        arciba_txt_generator.add_line_with_args(*asdict(l).values())
    return arciba_txt_generator.build()