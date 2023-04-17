# -*- coding: utf-8 -*-
from odoo import  fields, _
from odoo.fields import  One2many, Many2many, Many2one, Date, Float, Char, Text, Selection
from odoo.api import depends, onchange, returns, model
from odoo.models import Model, TransientModel

import logging
_logger = logging.getLogger(__name__)

def add_value_to_key(grouping_dict, key, value):
    old_val = grouping_dict.get(key, 0)
    grouping_dict.update({
        key: value + old_val
    })
    return grouping_dict

class PaymentGroup(Model):
    """Group payments into one model many payments can be reconciled to many invoices and print it in the same report.

    Possible cases:
    1 payment to 1 invoice fully payed
    1 Payment partially pays 1 invoice
    1 payment pays more than 1 invoice invoices leaving a balance in favor of the customer
    More than 1 payment pays more than 1 invoice
    More than 1 payments pays more than 1 invoice but leaves a balance in favor of the customer.
    More than 1 payments pays more than 1 invoice but 1 of the invoice is not fully payed.
    
    """

    _name = 'account.payment.group'
    _description = 'Groups different lines of account.payment and relates them with account.move lines (invoices, and other)'
    _inherit = 'mail.thread'
    _order = "date desc"
    
    company_id = fields.Many2one(
        'res.company',
        string='Company',
        required=True,
        index=True,
        change_default=True,
        default=lambda self: self.env.company,
        readonly=True,
        states={'draft': [('readonly', False)]},
    )
    name = Char(string="Nombre", readonly=1)
    sequence_id = Many2one('ir.sequence',string="Secuencia", default=lambda self: self.env.ref('account_payments_group.ir_sequence_account_payments_group'))
    state = Selection([('draft','Borrador'),('posted','Validado'),('canceled','Cancelado')],default="draft", string="Estado")

    payment_lines_ids = One2many('account.payment','payment_group_id', string="Pagos")
    move_line_ids = Many2many('account.move.line',string="Comprobantes imputados", states={'posted':[('readonly',True)]}) 
    currency_id = Many2one('res.currency',string="Moneda", default=lambda self: self.env.company.currency_id, required=True)
    company_id = Many2one('res.company',string="Compañia", default=lambda self: self.env.company, required=True)
    partner_id = Many2one('res.partner', string="Contacto", required=True)
    date = Date(string='Fecha',required=True, default=Date.today())
    observations = Text(string='Observaciones')
    payments_total = Float(string="Monto pago",compute="_compute_payments_total")
    unpaid_amount = Float(string="Monto adeudado",compute="_compute_matched_amount", store=True)
    matched_amount = Float(string="Importe imputado", compute="_compute_matched_amount", store=True)
    unmatched_amount = Float(string="Importe no imputado", compute="_compute_matched_amount", store=True)
    payment_difference_handling = fields.Selection([
        ('open', 'Keep open'),
        ('reconcile', 'Mark as fully paid'),
    ], default='open', string="Payment Difference Handling")
    writeoff_account_id = fields.Many2one('account.account', string="Difference Account", copy=False,
        domain="[('deprecated', '=', False), ('company_id', '=', company_id)]", limit=1)
    writeoff_journal_id = fields.Many2one('account.journal', string="Difference Journal", copy=False,
        domain="[('company_id', '=', company_id)]", required=True, default=lambda s: s.env['account.journal'].search([('type','=','general')], limit=1))
    writeoff_label = fields.Char(string='Journal Item Label', default='Write-Off',
        help='Change label of the counterpart that will hold the payment difference')

    def _get_closing_entry_move_lines(self, account_id, currency_id, balance):
        return  [
                (0,0,{
                    'name': self.writeoff_label,
                'amount_currency': -balance,
                'currency_id': currency_id,
                'debit': -balance if balance < 0.0 else 0.0,
                'credit': balance if balance > 0.0 else 0.0,
                'partner_id': self.partner_id.id,
                'account_id': account_id,
                }),
                (0,0,{
                'name': self.writeoff_label,
                'amount_currency': balance,
                'currency_id': currency_id,
                'debit': balance if balance > 0.0 else 0.0,
                'credit': -balance if balance < 0.0 else 0.0,
                'partner_id': self.partner_id.id,
                'account_id': self.writeoff_account_id.id,
            })]
    def _create_and_post_account_move(self, line_vals_list, currency_id):
        account_move = self.env['account.move'].create([{
                'partner_id':self.partner_id.id,
                'journal_id':self.writeoff_journal_id.id,
                'line_ids':line_vals_list,
                'move_type':'entry',
                'currency_id':currency_id
            }])
        account_move.action_post()
        return account_move

    def _create_payment_closing_entry(self):
        """Get the write off data, make a move id against the invoices to"""
        self.ensure_one()
        payment_lines = self.payment_lines_ids.move_id.line_ids.filtered(lambda r: not r.reconciled and r.account_id.reconcile and r.account_id.account_type == 'asset_receivable')
        balance = sum((payment_lines|self.move_line_ids).mapped('amount_residual')) 
        debt_account_id = self.move_line_ids.account_id.id
        if not self.currency_id.is_zero(balance):
            line_vals_list = self._get_closing_entry_move_lines(debt_account_id, self.currency_id.id, balance)
            return self._create_and_post_account_move(line_vals_list, self.currency_id.id)
            
        return self.env['account.move']

    def _create_foreign_currency_closing_entry_and_reconcile(self):
        self.ensure_one()
        moves_with_residual_currency = self.move_line_ids.filtered(lambda r: not self.currency_id.is_zero(r.amount_residual_currency))
        grouping_dict = {}
        for move in moves_with_residual_currency:
            grouping_dict = add_value_to_key(grouping_dict, move.currency_id.id, move.amount_residual_currency)
        for currency, value in grouping_dict.items():
            moves_for_this_currency = moves_with_residual_currency.filtered(lambda r:r.currency_id.id == currency)
            line_vals_list = self._get_closing_entry_move_lines(moves_for_this_currency.account_id.id , currency, value)
            closing_moves = self._create_and_post_account_move(line_vals_list, currency)
            # ? Maybe this shouldnt be this way.
            (moves_for_this_currency|closing_moves.line_ids).filtered(lambda r: not r.reconciled and r.account_id.reconcile and r.account_id.account_type == 'asset_receivable').reconcile()

    def post(self):
        for rec in self:
            payments = rec.payment_lines_ids
            payments.action_post()
            move_lines = self.env['account.move.line']
            filter_moves_to_reconcile = lambda r: not r.reconciled and r.account_id.reconcile and r.account_id.account_type == 'asset_receivable'
            move_lines |= (rec.move_line_ids | payments.line_ids).filtered(filter_moves_to_reconcile) 
            move_lines.filtered(filter_moves_to_reconcile).reconcile()
            if rec.payment_difference_handling == 'reconcile':
                """Two things should be done here. First we close the accounting balance. Next we close the currency balance for each invoice."""
                move_lines |= rec._create_payment_closing_entry().line_ids
                move_lines.filtered(filter_moves_to_reconcile).reconcile()
                rec._create_foreign_currency_closing_entry_and_reconcile()
            name = rec.name
            if not name:
                name = rec.sequence_id.next_by_id()
                rec.name = name
            for p in payments:
                p.ref = name
            rec.state = 'posted'

    def cancel(self):
        for rec in self:
            payments = rec.payment_lines_ids
            payments.action_draft()
            rec.state = 'canceled'
    
    def to_draft(self):
        for rec in self:
            rec.state = 'draft'

    @returns('account.move')
    def _get_unconcilied_move_line_ids(self):
        account_moves = self.env['account.move.line'].search([
            ('partner_id','=',self.partner_id.id),
            ('move_id.state','=','posted'),
            '|',('amount_residual','!=',0),('amount_residual_currency', '!=', 0.0),
            ('account_id.reconcile', '=', True),  
            ('account_id.deprecated', '=', False),
            ('account_id.account_type', '=', 'asset_receivable'),
            ('reconciled', '=', False)])
        return account_moves
        

    def add_all_unreconcilied_moves(self):
        for rec in self:
            move_line_ids = rec._get_unconcilied_move_line_ids().ids
            rec.move_line_ids = [(6,0,move_line_ids)]
    
    def remove_all_moves(self):
        for rec in self:
            rec.move_line_ids = [(5,0,0)]

    @onchange('partner_id')
    def _onchange_partner_id(self):
        for rec in self:
            if rec.partner_id:
                rec.add_all_unreconcilied_moves()
                rec.payment_lines_ids = False
                

    @depends('payment_lines_ids')
    def _compute_payments_total(self):
        for rec in self:
            rec.payments_total = sum(rec.payment_lines_ids.mapped('amount'))
            
    @depends('payments_total','move_line_ids','state')
    def _compute_matched_amount(self):
        for rec in self:
            unreconciled_partner_amls = self._get_unconcilied_move_line_ids()
            unpaid_amount = sum(unreconciled_partner_amls.mapped('amount_residual'))
            amls = rec.move_line_ids
            amount_residual = sum(amls.mapped('amount_residual'))
            payments = rec.payments_total
            matched_amount = 0
            if rec.state == 'posted':
                matched_amount = rec.matched_amount
            else:
                matched_amount = payments if payments <= amount_residual else amount_residual
            rec.write({
                'unpaid_amount':unpaid_amount,
                'unmatched_amount':amount_residual,
                'matched_amount':matched_amount
            })
