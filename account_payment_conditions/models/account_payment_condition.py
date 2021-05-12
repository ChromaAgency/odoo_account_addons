# -*- coding: utf-8 -*-
from odoo.api import onchange,model
from odoo.fields import Char, Many2many, Many2one
from odoo.models import Model

class PaymentConditions(Model):
  _name = "account.payment.condition"

  name = Char(string="Nombre")
  payment_terms_ids = Many2many('account.payment.term', string="Terminos de pago")
  
