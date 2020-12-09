# -*- coding: utf-8 -*-
from odoo.models import Model
from odoo.fields import Char
from odoo.tools import safe_eval
import logging
_logger = logging.getLogger(__name__)
class AccountMove(Model):
    _inherit = "account.move"
    
    def action_convert_currency(self):
        self.ensure_one()
        action = self.env.ref('account_currency_conversion.currency_conversion_invoice_wizard_action').read()[0]
        new_context = dict(safe_eval(action.get('context',{})),active_ids=self.ids,default_source_currency=self.currency_id.id)
        action.update({'context':new_context})
        return action