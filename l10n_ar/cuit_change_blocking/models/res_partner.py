from odoo.models import Model 
from odoo.fields import Boolean, Monetary
from odoo.exceptions import UserError
from odoo.api import model

class ResPartner(Model):
    _inherit = 'res.partner'

    vat_locked = Boolean(string='CUIT bloqueado?', default=True)

    def action_toggle_vat_lock(self):
        self.vat_locked = not self.vat_locked

    @model
    def _commercial_fields(self):
            return super(ResPartner, self)._commercial_fields() + ['vat_locked']

    def write(self, vals):
        _ = True
        if 'vat' not in vals:
            return super().write(vals)
        vat = vals.get("vat", False)
        for rec in self:
            if vat != rec.vat and rec.vat_locked:
                raise UserError('No se puede modificar el CUIT de un cliente')
        _ = super().write(vals)
        return _
    