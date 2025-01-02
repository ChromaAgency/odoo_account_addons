import base64
from odoo.models import TransientModel 
from odoo.fields import Binary, Char, Date, Integer, Many2one, Selection, Text, Boolean
from odoo.api import depends
import logging
_logger = logging.getLogger(__name__)
class UpdateArcibaResPartner(TransientModel):
    _name = "update.arciba.res.partner"
    _description = "Subir Padron de Arciba"

    file = Binary( string='Archivo de Padron a subir', required=True)
    file_name = Char( string='File Name', required=True)

    def _reset_arciba_res_partner(self):
        ResPartner = self.env['res.partner']
        partners = ResPartner.search([('is_arciba_res_partner', '=', True)])
        partners.write({
            'is_arciba_res_partner': False,
            })
        
    def _update_new_arciba_res_partner(self):
        ResPartner = self.env['res.partner']
        file_content = base64.b64decode(self.file).decode('latin1')
        lines = file_content.split('\n')
        vat_list = [line.split(';')[3].strip() for line in lines if len(line.split(';')) > 3]
        formatted_vat_list = list(map(lambda vat: f"{vat[:2]}-{vat[2:10]}-{vat[10:]}", vat_list))
        partners = ResPartner.search(['|',('vat', 'in', vat_list), ('vat', 'in', formatted_vat_list)])
        partners.write({
            'is_arciba_res_partner': True,
            })

    def update_arciba_res_partner(self):
        self.ensure_one()
        self._reset_arciba_res_partner()
        self._update_new_arciba_res_partner()
        
