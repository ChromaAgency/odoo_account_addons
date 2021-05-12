# -*- coding: utf-8 -*-
from odoo import _
from odoo.api import depends, model, onchange
from odoo.fields import Boolean, Char, Many2many, Many2one
from odoo.models import Model, TransientModel

class SaleOrder(Model):
  _name = "sale.order"
  _inherit = ["sale.order", "account.payment.condition.mixin"]

  @onchange('partner_id')
  def onchange_partner_id(self):
    super(SaleOrder, self).onchange_partner_id()
    self.payment_condition_id = self.partner_id.payment_condition_id
    self.payment_acquirer_id = self.partner_id.payment_acquirer_id
  def _prepare_invoice(self):
    invoice_vals = super(SaleOrder, self)._prepare_invoice()

    invoice_vals.update({
      'payment_condition_id':self.payment_condition_id.id,
      'payment_acquirer_id':self.payment_acquirer_id.id
    })
    return invoice_vals
    
class SaleAdvancePaymentInv(TransientModel):
  _inherit = "sale.advance.payment.inv"

  def _prepare_invoice_values(self, order, name, amount, so_line):
    invoice_vals = super(SaleAdvancePaymentInv, self)._prepare_invoice_values(order, name, amount, so_line)

    invoice_vals.update({
      'payment_condition_id':order.payment_condition_id.id,
      'payment_acquirer_id':order.payment_acquirer_id.id
    })
    return invoice_vals
    