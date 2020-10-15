# -*- coding: utf-8 -*-
from odoo.models import Model, TransientModel
from odoo.fields import Monetary, Char, Many2one, Float, Date
from odoo.exceptions import UserError
import ast
""" 
def open_action(self):
        #return action based on type for related journals
        action_name = self._context.get('action_name')

        # Find action based on journal.
        if not action_name:
            if self.type == 'bank':
                action_name = 'action_bank_statement_tree'
            elif self.type == 'cash':
                action_name = 'action_view_bank_statement_tree'
            elif self.type == 'sale':
                action_name = 'action_move_out_invoice_type'
            elif self.type == 'purchase':
                action_name = 'action_move_in_invoice_type'
            else:
                action_name = 'action_move_journal_line'

        # Set 'account.' prefix if missing.
        if '.' not in action_name:
            action_name = 'account.%s' % action_name

        action = self.env.ref(action_name).read()[0]
        context = self._context.copy()
        if 'context' in action and type(action['context']) == str:
            context.update(ast.literal_eval(action['context']))
        else:
            context.update(action.get('context', {}))
        action['context'] = context
        action['context'].update({
            'default_journal_id': self.id,
            'search_default_journal_id': self.id,
        })

        domain_type_field = action['res_model'] == 'account.move.line' and 'move_id.type' or 'type' # The model can be either account.move or account.move.line

        # Override the domain only if the action was not explicitly specified in order to keep the
        # original action domain.
        if not self._context.get('action_name'):
            if self.type == 'sale':
                action['domain'] = [(domain_type_field, 'in', ('out_invoice', 'out_refund', 'out_receipt'))]
            elif self.type == 'purchase':
                action['domain'] = [(domain_type_field, 'in', ('in_invoice', 'in_refund', 'in_receipt'))]

        return action """

class AccountJournal(Model):
    _inherit = 'account.journal'


    def add_new_moves_simplified(self):
        """
        This function should open a window where you add a movement with date, label, type, and amount.
        Types should be taken from a model that relate type to account in the other end (ex if cash is the journal account, and amount is neg, it should make a move where cash is the credit account wth x ammount and the type.account_id is the debit with x amount, and the other way around if it is positive).
        """
        action = self.env.ref('account_move_simplified_management.action_account_add_move_view_form_simplified_management').read()[0]
        
        context = self._context.copy()
        if 'context' in action and type(action['context']) == str:
            context.update(ast.literal_eval(action['context']))
        else:
            context.update(action.get('context', {}))
        action['context'] = context
        action['context'].update({
            'default_journal_id':self.id,
            'default_currency_id':self.currency_id.id or self.env.company.currency_id.id,
        })

        return action
    def view_moves_simplified(self):
        action = self.env.ref('account_move_simplified_management.action_account_move_line_view_list_simplified_management').read()[0]
        
        context = self._context.copy()
        # context.update({'search_default_my_appointments':1})
        if 'context' in action and type(action['context']) == str and len(action['context'])>0:
            context.update(ast.literal_eval(action.get('context', {})))
        else:
            context.update(action.get('context', {}))
        action['context'] = context

        domain = [('journal_id','=',self.id),('account_id','in',[self.default_debit_account_id.id, self.default_credit_account_id.id])]
        if 'domain' in action and type(action['domain']) == str:
            domain += ast.literal_eval(action['domain'])
        action['domain'] = domain

        return action

class AccountMoveGenerator(TransientModel):
    _name = 'account.move.simplified'

    def _get_default_move_type(self):
        return self.env['account.move.simplified.type'].search([])[0]

    date = Date(string="Fecha", required=True, default=Date.today())
    name = Char(string="Descripcion", required=True)
    amount = Float('Importe', required=True, default=0.0)
    journal_id = Many2one('account.journal',string="Metodo de pago", required=True)
    move_type = Many2one('account.move.simplified.type',string="Tipo", required=True, default=_get_default_move_type)
    currency_id = Many2one('res.currency',string="Moneda", required=True)

    def _create_move_line(self):
        amount = self.amount
        journal = self.journal_id
        account = self.move_type.account_id
        if not account.id:
            UserError('No hay cuenta definida para el tipo de pago')
            return
        name = self.name
        cash_item = {
                'account_id':account.id,
                'name':name
        }
        entry_item = {
                'name':name
        }
        if amount == 0:
            UserError('Monto no debe ser 0')
        elif amount < 0:
            credit_account = journal.default_credit_account_id
            amount = -1*amount
            entry_item.update({
                'credit':amount,
                'account_id':credit_account.id,
                
            })
            cash_item.update({
                'debit':amount,
            })
        else:
            debit_account = journal.default_debit_account_id
            cash_item.update({
                'credit':amount,
            })
            entry_item.update({
                'debit':amount,
                'account_id':debit_account.id
            })
        return [entry_item,cash_item]
    def _get_move_lines(self):
        lines = []
        lines += self._create_move_line()
        return lines
        
    def create_move_lines(self):
        # raise UserError('Que onda? {}'.format(self.amount))
        for rec in self:
            lines = rec._get_move_lines()
            line_ids = []
            for line in lines:
                line_ids.append((0,0,line))
                
            vals_list = [{
                'date':rec.date,
                'extract_state':'no_extract_requested',
                'type':'entry',
                'journal_id':rec.journal_id.id,
                'currency_id':rec.currency_id.id,
                'line_ids':line_ids,
                # 'name':'/'
            }]
            move = self.env['account.move'].create(vals_list)
            move.post()

        

class accountMoveSimplifiedType(Model):
    _name = 'account.move.simplified.type'

    name = Char(string="Nombre", required=True)
    account_id = Many2one('account.account',string="Cuenta relacionada", required=True)