# -*- coding: utf-8 -*-
from odoo import _
from odoo.api import onchange,model
from odoo.fields import Boolean, Char, Many2many, Many2one
from odoo.models import Model

class PaymentConditions(Model):
  _name = "account.payment.condition"

  name = Char(string=_("Nombre"))
  payment_terms_ids = Many2many('account.payment.term', string=_("Terminos de pago"))
  payment_acquirer_ids = Many2many('payment.acquirer', string=_("Añade metodo de pago"))
