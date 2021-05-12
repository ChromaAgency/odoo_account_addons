# -*- coding: utf-8 -*-
from odoo.api import depends, model, onchange
from odoo.fields import Boolean, Char, Many2many, Many2one
from odoo.models import Model

class SaleOrder(Model):
  _inherit = "sale.order"

  payment_condition_id = Many2one('account.payment.condition', string="Condicion de pago")
  possible_payment_terms = Many2many(related="payment_condition_id.payment_terms_ids")
  is_payment_term_id_visible = Boolean(string="Terminos de pago visibles", compute="_compute_is_payment_term_id_visible")

  @depends('possible_payment_terms', 'payment_condition_id')
  def _compute_is_payment_term_id_visible(self):
    for rec in self:
      rec.is_payment_term_id_visible = False
      if rec.payment_condition_id != False and len(rec.possible_payment_terms) > 1:
        rec.is_payment_term_id_visible = True
      elif len(rec.possible_payment_terms) == 1:
        rec.payment_term_id = rec.possible_payment_terms.id
      else:
        rec.payment_term_id = False
        
  def onchange_partner_id(self):
    super(SaleOrder, self).onchange_partner_id()
    self.payment_condition_id = self.partner_id.payment_condition_id
    