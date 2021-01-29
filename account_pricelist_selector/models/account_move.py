from odoo.models import Model
from odoo.fields import Many2one
from odoo.api import onchange,model

class AccountMove(Model):
  _inherit = "account.move"

  @model
  def _get_default_pricelist_id(self): 
    if self.type in ['in_invoice','in_refund']:
      return False
    return self.partner_id.property_product_pricelist.id

  pricelist_id = Many2one('product.pricelist',default=_get_default_pricelist_id,string="Lista de precios",check_company=True,  # Unrequired company
        readonly=True, states={'draft': [('readonly', False)], 'sent': [('readonly', False)]},
        domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]",
        help="If you change the pricelist, only newly added lines will be affected.")


  @model
  def create(self,vals):
    if not 'pricelist_id' in vals:
      partner = self.env['res.partner'].browse(vals.get('partner_id'))
      vals.update({
        'pricelist_id':  vals.setdefault('pricelist_id', partner.property_product_pricelist and partner.property_product_pricelist.id)

      })
    account_move = super(AccountMove,self).create(vals)
    return account_move

  @onchange('pricelist_id')
  def _onchange_pricelist_id(self):
    if self.pricelist_id:
      self.ensure_one()
      for line in self.invoice_line_ids:
        if line.product_id:
          line.price_unit = self.pricelist_id.get_product_price(line.product_id,line.quantity,self.partner_id)
          line._onchange_price_subtotal()
      
      self._onchange_invoice_line_ids()