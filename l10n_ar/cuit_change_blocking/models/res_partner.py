from odoo.models import Model 
from odoo.fields import Boolean, Monetary
from odoo.exceptions import UserError

class ResPartner(Model):
    _inherit = 'res.partner'

    vat_locked = Boolean(string='CUIT bloqueado?', default=True)

    def action_toggle_vat_lock(self):
        self.vat_locked = not self.vat_locked

    def write(self, vals):
        _ = True
        for rec in self:
            if 'vat' in vals and rec.vat_locked:
                raise UserError('No se puede modificar el CUIT de un cliente')
            _ = super().write(vals)
        return _