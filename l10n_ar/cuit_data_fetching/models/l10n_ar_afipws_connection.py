from odoo.models import Model
from odoo.api import model
from ..constants import CONSTANCIA_DE_INSCRIPCION_WS
class L10nArAfipwsConnection(Model):

    _inherit = "l10n_ar.afipws.connection"

    def _get_l10n_ar_afip_ws(self):
        return super()._get_l10n_ar_afip_ws() + self.env['res.partner']._get_l10n_ar_afip_ws()
    
    @model
    def _l10n_ar_get_afip_ws_url(self, afip_ws, environment_type):
        url = super()._l10n_ar_get_afip_ws_url(afip_ws, environment_type)
        if not url:
            ws_data = {
                CONSTANCIA_DE_INSCRIPCION_WS: {
                    'testing': 'https://awshomo.afip.gov.ar/sr-padron/webservices/personaServiceA5?wsdl',
                    'production': 'https://aws.afip.gov.ar/sr-padron/webservices/personaServiceA5?wsdl',
                }
            }
            return ws_data.get(afip_ws, {}).get(environment_type)
            
        return url
