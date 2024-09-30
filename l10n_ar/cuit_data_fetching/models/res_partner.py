from odoo import _
from odoo.exceptions import UserError
from odoo.models import Model 
from odoo.fields import Text
from ..constants import CONSTANCIA_DE_INSCRIPCION_WS, RESPONSABLE_INSCRIPTO, IVA_SUJETO_EXENTO, CONSUMIDOR_FINAL, RESPONSABLE_MONOTRIBUTO, IVA_LIBERADOR_SEGUN_LEY, IVA_NO_ALCANZADO

import logging
_logger = logging.getLogger(__name__)

class ResPartner(Model):
    _inherit = 'res.partner'

    cuit_update_error = Text(string="Error de actualización de CUIT")
    @property
    def ar_state_map(self):
        return {
        0 : self.env.ref('base.state_ar_c').id,
        1 : self.env.ref('base.state_ar_b').id,
        2 : self.env.ref('base.state_ar_k').id,
        16 : self.env.ref('base.state_ar_h').id,
        17 : self.env.ref('base.state_ar_u').id,
        3 : self.env.ref('base.state_ar_x').id,
        4 : self.env.ref('base.state_ar_w').id,
        5 : self.env.ref('base.state_ar_e').id,
        18 : self.env.ref('base.state_ar_p').id,
        6 : self.env.ref('base.state_ar_y').id,
        21 : self.env.ref('base.state_ar_l').id,
        8 : self.env.ref('base.state_ar_f').id,
        7 : self.env.ref('base.state_ar_m').id,
        19 : self.env.ref('base.state_ar_n').id,
        20 : self.env.ref('base.state_ar_q').id,
        22 : self.env.ref('base.state_ar_r').id,
        9 : self.env.ref('base.state_ar_a').id,
        10 : self.env.ref('base.state_ar_j').id,
        11 : self.env.ref('base.state_ar_d').id,
        23 : self.env.ref('base.state_ar_z').id,
        12 : self.env.ref('base.state_ar_s').id,
        13 : self.env.ref('base.state_ar_g').id,
        24 : self.env.ref('base.state_ar_v').id,
        14 : self.env.ref('base.state_ar_t').id,
        }

    def _get_l10n_ar_afip_ws(self):
        """ Return the list of values of the selection field. """
        #TODO super()._get_l10n_ar_afip_ws() + 
        return [(CONSTANCIA_DE_INSCRIPCION_WS, _('CUIT Data fetching'))] 

    def get_partner_data_with_cuit(self):
        self.ensure_one()
        if self.l10n_latam_identification_type_id.name == 'CUIT':
            cuit = self.vat
            if self.country_id.id != self.env.ref('base.ar').id:
                raise UserError(_("This partner is not from Argentina."))
            if not cuit:
                raise UserError(_("You must set a CUIT number for this partner."))
            
            connection = self.env.company._l10n_ar_get_connection(CONSTANCIA_DE_INSCRIPCION_WS)
            client, auth = connection._get_client()
            try:
                res = client.service.getPersona_v2(auth.get('Token'),auth.get('Sign'),auth.get('Cuit'),cuit)
            except:
                raise UserError(_("The provided CUIT is not valid."))
            self._update_partner_data(res)
        else:
            raise UserError(_("The provided number is not a CUIT."))
        return True
        
        
    def _update_partner_data(self, partner_data):
        if not partner_data:
            raise UserError(_("No data was found for this CUIT. %s" % partner_data))
        if not partner_data['datosGenerales']:
            raise UserError(_("No datosGenerales was found. %s" % partner_data))
        address_info = partner_data['datosGenerales']['domicilioFiscal']
        postal_code = address_info['codPostal']
        province = address_info['idProvincia']
        street = address_info['direccion']
        cuit_type = partner_data['datosGenerales']['tipoClave']
        
        afip_responsibility = self._check_afip_responsability(partner_data, province)

        cuit_type = self.env['l10n_latam.identification.type'].search([('name','=',cuit_type)]).id
        self.write({
            'street': street,
            'zip': postal_code,
            'l10n_ar_afip_responsibility_type_id': afip_responsibility,
            'l10n_latam_identification_type_id': cuit_type,
            'state_id': self.ar_state_map.get(province, False)


        })

        

    def _check_afip_responsability(self, partner_data, province):
        generalregimen_data = partner_data['datosRegimenGeneral']
        monotributo_data = partner_data['datosMonotributo']

        if generalregimen_data:
            for tax in generalregimen_data['impuesto']:
                if tax['idImpuesto'] == 34:
                    return IVA_NO_ALCANZADO
                if tax['idImpuesto'] == 32:
                    return IVA_SUJETO_EXENTO
                if province == 24:
                    return IVA_LIBERADOR_SEGUN_LEY
            return RESPONSABLE_INSCRIPTO
        if monotributo_data:
            return RESPONSABLE_MONOTRIBUTO
        return CONSUMIDOR_FINAL