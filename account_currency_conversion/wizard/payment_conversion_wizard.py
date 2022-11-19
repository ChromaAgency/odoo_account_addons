
# -*- coding: utf-8 -*-
from odoo.models import TransientModel
from odoo.fields import Float
from odoo.exceptions import UserError
from odoo import _
import logging

class PaymentCurrencyConversion(TransientModel):
  _name="res.currency.conversion.payment.wizard"
  _description = "Conversion de moneda en pago"
  _inherit = "res.currency.conversion.wizard"
  
  def confirm(self):
    self.ensure_one()
    ctx = self._context
    active_ids = ctx.get('active_ids')
    super(PaymentCurrencyConversion,self).confirm()
    payments = self.env['account.payment'].browse(active_ids)
    # for payment in payments:
    #   if payment.state in ['posted','sent','reconciled']:
    #     raise UserError(_('You cant change an already posted invoice'))
    
    return {'type': 'ir.actions.act_window_close'}


