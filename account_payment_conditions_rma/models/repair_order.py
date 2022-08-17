# -*- coding: utf-8 -*-
from odoo import _
from odoo.api import depends, model, onchange
from odoo.fields import Boolean, Char, Many2many, Many2one
from odoo.models import Model, TransientModel

class RepairOrder(Model):
  _name = "repair.order"
  _inherit = ["repair.order", "account.payment.condition.mixin"]

  payment_term_id = Many2one('account.payment.term', string="Plazo de pago")

  @onchange('partner_id')
  def onchange_partner_id(self):
    super(RepairOrder, self).onchange_partner_id()
    self.payment_term_id = self.partner_id.property_payment_term_id
    self.payment_condition_id = self.partner_id.payment_condition_id
    self.payment_acquirer_id = self.partner_id.payment_acquirer_id

  def _create_invoices(self, group=False):
    repair_invoice_dict = super(RepairOrder, self)._create_invoices(group=False)
    for repair, invoice in repair_invoice_dict.items():
          repair_order = self.browse([repair])
          self.env['account.move'].browse([invoice]).write({
            'invoice_payment_term_id':repair_order.payment_term_id.id,
            'payment_condition_id':repair_order.payment_condition_id.id,
            'payment_acquirer_id':repair_order.payment_acquirer_id.id
          })
    return repair_invoice_dict
