from odoo import models, api, fields

class ResPartner(models.Model):
    _inherit = 'res.partner'

    is_arciba_res_partner = fields.Boolean(string='Es un Responsable de Arciba', default=False)

    def action_update_arciba_res_partner(self):
        action = self.env.ref('l10n_ar_withholdings_afip_txt.action_update_arciba_res_partner')
        return action.read()[0]
