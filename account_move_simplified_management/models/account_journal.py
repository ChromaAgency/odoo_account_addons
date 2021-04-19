# -*- coding: utf-8 -*-
from odoo.exceptions import UserError
from odoo.fields import Char, Date, Float, Many2one, Monetary
from odoo.models import Model, TransientModel
from odoo.tools.convert import safe_eval

class AccountJournal(Model):
    _inherit = 'account.journal'


    def add_new_expenses_simplified(self):
        """
        This function should open a window where you add a movement with date, label, type, and amount.
        Types should be taken from a model that relate type to account in the other end (ex if cash is the journal account, and amount is neg, it should make a move where cash is the credit account wth x ammount and the type.account_id is the debit with x amount, and the other way around if it is positive).
        """
        action = self.env.ref('account_move_simplified_management.action_account_add_move_view_form_simplified_management').read()[0]
        
        context = self._context.copy()
        context.update(safe_eval(action['context']))
        action['context'] = context
        action['context'].update({
            'move_type':'egress',
            'default_journal_id':self.id,
            'default_currency_id':self.currency_id.id or self.env.company.currency_id.id,
        })
        action.update({
            'name': 'Agregar Egreso'
        })
        return action

    def add_new_incomes_simplified(self):
        """
        This function should open a window where you add a movement with date, label, type, and amount.
        Types should be taken from a model that relate type to account in the other end (ex if cash is the journal account, and amount is neg, it should make a move where cash is the credit account wth x ammount and the type.account_id is the debit with x amount, and the other way around if it is positive).
        """
        action = self.env.ref('account_move_simplified_management.action_account_add_move_view_form_simplified_management').read()[0]
        
        context = self._context.copy()
        if 'context' in action and type(action['context']) == str:
            context.update(safe_eval(action['context']))
        else:
            context.update(action.get('context', {}))
        action['context'] = context
        action['context'].update({
            'move_type':'income',
            'default_journal_id':self.id,
            'default_currency_id':self.currency_id.id or self.env.company.currency_id.id,
        })
        action.update({
            'name': 'Agregar Ingreso'
        })
        return action
        
    def view_moves_simplified(self):
        action = self.env.ref('account_move_simplified_management.action_account_move_line_view_list_simplified_management').read()[0]
        
        context = self._context.copy()
        context.update({'search_default_posted':1})
        context.update(safe_eval(action.get('context', {})))
        action['context'] = context
        domain = [('journal_id','=',self.id),('account_id','in',[self.default_debit_account_id.id, self.default_credit_account_id.id])]
        if 'domain' in action and type(action['domain']) == str:
            domain += ast.literal_eval(action['domain'])
        action['domain'] = domain
        return action
