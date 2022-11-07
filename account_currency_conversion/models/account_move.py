# -*- coding: utf-8 -*-
from odoo.models import Model
from odoo.fields import Char,Float
from odoo.api import depends
from ast import literal_eval
import logging
_logger = logging.getLogger(__name__)
class AccountMove(Model):
    _inherit = "account.move"
    
    exchange_rate = Float(string="Tipo de cambio", compute="_compute_currency_rate")

    def _compute_currency_rate(self):
        for rec in self:
            rec.exchange_rate = 1/rec.currency_id.rate

    def action_convert_currency(self):
        self.ensure_one()
        action = self.env.ref('account_currency_conversion.currency_conversion_invoice_wizard_action').sudo().read()[0]
        new_context = dict(literal_eval(action.get('context',{})),active_ids=self.ids,default_source_currency=self.currency_id.id)
        action.update({'context':new_context})
        return action
