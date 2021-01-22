# -*- coding: utf-8 -*-
from odoo.models import Model, TransientModel
from odoo.fields import Monetary, Char, Many2one, Float, Date
from odoo.exceptions import UserError
from odoo.tools.convert import safe_eval

class AccountJournal(Model):
    _inherit = 'account.move.line'

    move_simplified_type_id = Many2one('account.move.simplified.type',string="Tipo de cuenta simplificado", )

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
        move_type = self.move_type
        account = move_type.account_id
        
        if self._context['move_type'] == 'egress':
            amount *= -1
        if not account.id:
            raise UserError('No hay cuenta definida para el tipo de pago')
            return
        name = self.name
        cash_item = {
                'account_id':account.id,
                'name':name,
                'move_simplified_type_id':move_type.id
        }
        entry_item = {
                'name':name,
                'move_simplified_type_id':move_type.id
        }
        if amount == 0:
            raise UserError('Monto no debe ser 0')
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