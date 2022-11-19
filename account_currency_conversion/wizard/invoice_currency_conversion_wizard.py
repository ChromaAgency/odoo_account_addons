# -*- coding: utf-8 -*-
from odoo.models import TransientModel
from odoo.fields import Float
from odoo.exceptions import UserError
from odoo import _

class InvoiceCurrencyConversion(TransientModel):
  _name="res.currency.conversion.invoice.wizard"
  _description = "Conversion de moneda en factura"
  _inherit = "res.currency.conversion.wizard"
  
  def confirm(self):
    self.ensure_one()
    ctx = self._context
    active_ids = ctx.get('active_ids')
    account_moves = self.env['account.move'].browse(active_ids).with_context(check_move_validity=False)
    for am in account_moves:
      if am.state == 'posted':
        raise UserError(_('You cant change an already posted invoice'))
      for aml in am.line_ids: 
        aml.write({
            'price_unit': Float.round(aml.price_unit * self.exchange_rate, precision_rounding=self.target_currency.rounding),
            'currency_id':self.target_currency.id
        })
        aml._onchange_mark_recompute_taxes()
        aml._onchange_currency()
      am.currency_id = self.target_currency.id
      message = _("Currency changed from %s to %s with rate %s") % (am.currency_id.name, self.target_currency.name, self.exchange_rate)
      am.message_post(body=message)
      super(InvoiceCurrencyConversion,self).confirm()
    return {'type': 'ir.actions.act_window_close'}