# -*- coding: utf-8 -*-
from odoo.models import Model
from odoo.fields import Char,Float
from odoo.api import depends
from ast import literal_eval
import logging
_logger = logging.getLogger(__name__)

class AccountPayment(Model):
    _inherit = "account.payment"

    currency_id_rate = Float(related="currency_id.rate",string="Tipo de cambio de la moneda actual")
    exchange_rate = Float(string="Tipo de cambio actual",compute="_compute_exchange_rate")

    @depends('currency_id_rate')
    def _compute_exchange_rate(self):
        for payment in self:
            payment.exchange_rate = 1/payment.currency_id_rate
        

    def action_convert_currency(self):
        self.ensure_one()
        action = self.env.ref('account_currency_conversion.currency_conversion_payment_wizard_action').sudo().read()[0]
        new_context = dict(literal_eval(action.get('context',{})),active_ids=self.ids,default_source_currency=self.currency_id.id)
        action.update({'context':new_context})
        return action