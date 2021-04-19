# -*- coding: utf-8 -*-
from odoo.exceptions import UserError
from odoo.fields import Char, Date, Float, Many2one, Monetary
from odoo.models import Model, TransientModel
from odoo.tools.convert import safe_eval

class AccountJournal(Model):
    _inherit = 'account.move.line'

    move_simplified_type_id = Many2one('account.move.simplified.type',string="Tipo de cuenta simplificado", )

    def action_view_payment(self):
        self.ensure_one()
        action = self.env.ref('account_move_simplified_management.action_account_view_payment').read()[0]
        action.update({
            'res_id':self.payment_id.id
        })
        return action
        
    def button_simplified_cancel(self):
        self.ensure_one()
        self.move_id.button_cancel()
