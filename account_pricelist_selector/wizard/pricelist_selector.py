from odoo.models import TransientModel
from odoo.fields import Many2one
from odoo.api import onchange

class PricelistSelector(TransientModel):
  _name = 'account.move.pricelist.selector'
  _description = 'Pricelist Selector to change invoice prices at once'

  company_id = Many2one('res.company', default=lambda s:s.env.company)
  company_currency_id = Many2one('res.currency', related='company_id.currency_id')
  pricelist_id = Many2one('product.pricelist',string="Lista de precios")

  @onchange('pricelist_id')
  def _onchange_pricelist_id(self):
    pass