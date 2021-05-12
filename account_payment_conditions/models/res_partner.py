# -*- coding: utf-8 -*-
from odoo import _
from odoo.api import depends, model, onchange
from odoo.fields import Boolean, Char, Many2many, Many2one
from odoo.models import Model

class ResPartner(Model):
  _name = "res.partner"
  _inherit = ["res.partner", "account.payment.condition.mixin"]

  @model
  def _commercial_fields(self):
    return super(ResPartner, self)._commercial_fields() + ['payment_acquirer_id', 'payment_condition_id']