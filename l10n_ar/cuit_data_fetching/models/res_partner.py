from odoo import _
from odoo.exceptions import UserError
from odoo.models import Model 
from ..constants import CONSTANCIA_DE_INSCRIPCION_WS

import logging
_logger = logging.getLogger(__name__)

class ResPartner(Model):
    _inherit = 'res.partner'

    def _get_l10n_ar_afip_ws(self):
        """ Return the list of values of the selection field. """
        return super()._get_l10n_ar_afip_ws() + [(CONSTANCIA_DE_INSCRIPCION_WS, _('CUIT Data fetching'))] 

    def get_partner_data_with_cuit(self, cuit):
        self.ensure_one()
        cuit = self.vat
        if self.country_id.id != self.env.ref('base.ar').id:
            raise UserError(_("This partner is not from Argentina."))
        if not cuit:
            raise UserError(_("You must set a CUIT number for this partner."))
        
        connection = self.env.company._l10n_ar_get_connection(CONSTANCIA_DE_INSCRIPCION_WS)
        client, auth = connection._get_client()
        res = client.service.getPersona_v2(auth, {
            'token':auth.get("token"),
            'sign':auth.get("sign"),
            'cuitRepresentada':self.env.company.vat,
            'idPersona':cuit,

        })
        _logger.info(res)
        data = res.getPersona_v2Response.personaReturn
        address = data.domicilioFiscal
        cuit_type = data.tipoClave
        """ 
            si tiene datos monotributo return mono.
            si tiene datos general checkear 
                si es tierra del fuego return iva liberado
                si tiene iva exento en impuestos return iva exento
                si tiene iva no alcanzado  en impuestos return iva no alcanzado
                return responsable inscripto
                
            return consumidor final
        """
        afip_responsibility = ''
