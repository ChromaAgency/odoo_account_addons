# -*- coding: utf-8 -*-
from odoo import _
from odoo.api import depends, model, onchange
from odoo.fields import Boolean, Char, Many2many, Many2one
from odoo.models import Model, AbstractModel
import logging

_logger = logging.getLogger(__name__)

class ResPartnerPaymentMethod(Model):
    _name = "res.partner.payment.method"
    
    name = Char(string="Nombre")

class PaymentConditionMixin(AbstractModel):
  _name = "account.payment.condition.mixin"
  _description = 'Mixin de condiciones de pago'

  payment_condition_id = Many2one('account.payment.condition', string=_("Condicion de pago"))
  possible_payment_terms = Many2many(related="payment_condition_id.payment_terms_ids")
  is_payment_term_id_visible = Boolean(string=_("Terminos de pago visibles"), compute="_compute_is_payment_term_id_visible")
  possible_payment_acquirers = Many2many(related="payment_condition_id.payment_acquirer_ids")
  payment_acquirer_id = Many2one('res.partner.payment.method', string=_("Metodo de pago"))
  is_payment_acquirer_id_visible = Boolean(string=_("Es metodo de pago visible") , compute="_compute_is_payment_acquirer_id_visible")

  def write(self, vals):
      payment_condition_id = vals.get('payment_condition_id') 
      if payment_condition_id and 'payment_acquirer_id' not in vals:
            possible_acquirer_ids = self.env['account.payment.condition'].browse(payment_condition_id).payment_acquirer_ids
            if len(possible_acquirer_ids) == 1:
                  vals.update({
                    'payment_acquirer_id':possible_acquirer_ids.id
                  })
      return super().write(vals)

  @onchange('payment_condition_id')
  def _onchange_payment_condition_id(self):
      len_of_payment = self.payment_condition_id.payment_acquirer_ids
      _logger.info(len_of_payment)
      if len_of_payment == 1:
            self.payment_acquirer_id = self.payment_condition_id.payment_acquirer_ids.id

  @depends('possible_payment_acquirers', 'payment_condition_id')
  def _compute_is_payment_acquirer_id_visible(self):
    for rec in self:
      rec.is_payment_acquirer_id_visible = False
      if rec.payment_condition_id != False and len(rec.possible_payment_acquirers) >= 1:
        rec.is_payment_acquirer_id_visible = True

  @depends('possible_payment_terms', 'payment_condition_id')
  def _compute_is_payment_term_id_visible(self):
    if self._name == 'res.partner':
      payment_term_field_name = 'property_payment_term_id'  
    elif self._name == 'account.move':
      payment_term_field_name = 'invoice_payment_term_id'  
    else:
      payment_term_field_name = 'payment_term_id'
      
    for rec in self:
      rec.is_payment_term_id_visible = False
      if rec.payment_condition_id != False and len(rec.possible_payment_terms) > 1:
        rec.is_payment_term_id_visible = True
      elif len(rec.possible_payment_terms) == 1:
        setattr(rec, payment_term_field_name, rec.possible_payment_terms.id)
      else:
        setattr(rec, payment_term_field_name, False)

class PaymentConditions(Model): 
  _name = "account.payment.condition"
  _description = 'Condiciones de pago'

  active = Boolean(string="Activo", default=True)
  name = Char(string=_("Nombre"))
  payment_terms_ids = Many2many('account.payment.term', string=_("Terminos de pago"))
  payment_acquirer_ids = Many2many('res.partner.payment.method', string=_("Añade metodo de pago"))
