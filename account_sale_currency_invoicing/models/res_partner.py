from odoo.models import Model
from odoo.api import model
from odoo.fields import Many2one
class ResPartner(Model):
    _inherit = "res.partner"
    
    invoicing_currency = Many2one('res.currency',default=lambda s:s.env.company.currency_id.id,string='Moneda de facturación')
    
    @model
    def _commercial_fields(self):
        return super(ResPartner, self)._commercial_fields() + ['invoicing_currency']