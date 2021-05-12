# -*- coding: utf-8 -*-
from odoo import _
from odoo.api import depends, model, onchange
from odoo.fields import Boolean, Char, Many2many, Many2one
from odoo.models import Model

class AccountMove(Model):
  _name = "account.move"
  _inherit = ["account.move", "account.payment.condition.mixin"]
