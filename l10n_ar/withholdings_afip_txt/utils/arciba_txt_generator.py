from dataclasses import dataclass, field, asdict
from typing import Dict, List
from datetime import date
from .column_width_generator import FixedColumnWidthCSVGenerator

arciba_ret_per_cols = {
    "op_type":1,
    "norm":3,
    "retper_date":10,
    "doc_type":2,
    "doc_letter":1,
    "doc_number":16,
    "doc_date":10,
    "doc_amount":16,
    "ret_number":16,
    "afip_document_type":1,
    "afip_document_number":11,
    "ib_type":1,
    "ib_number":11,
    "iva_type":1,
    "name":30,
    "amount_other":16,
    "amount_iva":16,
    "base_amount_for_tax":16,
    "tax_rate":5,
    "tax_amount":16,
    "tax_retention":16,
}

def generate_arciba_txt_generator():
    arciba_txt_generator = FixedColumnWidthCSVGenerator()
    aligns = {
        float:"<",
        str:">",
    }
    fills = {
        str:" ",
        float:"0",
    }

    formats = {
        float:".2f",
        str:"",
        date:"%d/%m/%Y",
    }

    post_process_fn = {
        float:lambda x: x.replace(".", ",")
    }
    for name, t in vars(ArcibaTxtRetPercLine)['__annotations__'].items():
        arciba_txt_generator.add_column(formats.get(t, ""), aligns.get(t, ""), fills.get(t, ""), arciba_ret_per_cols[name], post_process_fn.get(t, lambda x: x))
    return arciba_txt_generator
        
@dataclass
class ArcibaTxtRetPercLine:
    """
    Spec according to V2 of e-Arciba 
    Source 2023: https://www.agip.gob.ar/filemanager/source/Agentes/DocTecnicoImpoOperacionesDise%C3%B1odeRegistro.pdf
    """
    op_type:str
    norm:str
    retper_date:date
    doc_type:str
    doc_letter:str
    doc_number:str
    doc_date:date
    doc_amount:float
    ret_number:str
    afip_document_type:str
    afip_document_number:str
    ib_type:str
    ib_number:str
    iva_type:str
    name:str
    amount_other:float
    amount_iva:float
    base_amount_for_tax:float
    tax_rate:float
    tax_amount:float
    tax_retention:float


    def add_line_to_generator(self, generator:FixedColumnWidthCSVGenerator):
        retper_date = self.retper_date
        doc_date = self.doc_date
        generator.add_line_with_args(self.op_type, self.norm, retper_date, self.doc_type, self.doc_letter, self.doc_number, doc_date, self.doc_amount, self.ret_number, self.afip_document_type, self.afip_document_number, self.ib_type, self.ib_number, self.iva_type, self.name, self.amount_other, self.amount_iva, self.base_amount_for_tax, self.tax_rate, self.tax_amount, self.tax_retention)

def build_and_generate_txt(lines:List[ArcibaTxtRetPercLine]):         
    arciba_txt_generator = generate_arciba_txt_generator()
    for l in lines:
        arciba_txt_generator.add_line_with_args(*asdict(l).values())
    return arciba_txt_generator.build()