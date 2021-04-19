# -*- coding: utf-8 -*-
from odoo.exceptions import UserError
from odoo.fields import Char, Date, Float, Many2one, Monetary
from odoo.models import Model, TransientModel
from odoo.tools.convert import safe_eval

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

    def _prepare_move_line_vals(self):
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
        
    def _prepare_move_lines(self):
        lines = []
        lines += self._prepare_move_line_vals()
        return lines
        
    def _prepare_move_vals(self):
        self.ensure_one()
        line_ids = [(0,0,line) for line in rec._prepare_move_lines()]                
        move_lines_vals = {
                'date':self.date,
                'extract_state':'no_extract_requested',
                'type':'entry',
                'journal_id':self.journal_id.id,
                'currency_id':self.currency_id.id,
                'line_ids':line_ids,
                # 'name':'/'
            }
        return move_lines_vals
        
    def create_move_lines(self):
        for rec in self:
            move = self.env['account.move'].create(rec._prepare_move_vals())
            move.post()

class accountMoveSimplifiedType(Model):
    _name = 'account.move.simplified.type'

    name = Char(string="Nombre", required=True)
    account_id = Many2one('account.account',string="Cuenta relacionada", required=True)