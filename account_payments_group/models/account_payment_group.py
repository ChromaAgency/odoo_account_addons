# -*- coding: utf-8 -*-
from sqlite3 import adapt
from odoo import  fields, _
from odoo.fields import  One2many, Many2many, Many2one, Date, Float, Char, Text, Selection
from odoo.api import depends, onchange, returns, model
from odoo.models import Model, TransientModel

import logging
_logger = logging.getLogger(__name__)



class AccountPayment(Model):
    _inherit = 'account.payment'
    
    payment_group_id = Many2one('account.payment.group', string="Payment Group")
    
    def _add_partner_id_to_vals(self, vals):
        if 'payment_group_id' not in vals or vals.get('partner_id' ):
            return vals
        partner_id = self.env['account.payment.group'].browse([vals.get('payment_group_id')]).partner_id.id
        vals.update({
            'partner_id':partner_id
        })
        return vals

    def _add_partner_id_from_group_id(self, vals_list):
        return [self._add_partner_id_to_vals(vals) for vals in vals_list] if isinstance(vals_list, list) else self._add_partner_id_to_vals(vals_list)

    @model
    def create(self, vals_list):
        self._add_partner_id_from_group_id(vals_list)
        return super().create(vals_list)

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
        domain="[('deprecated', '=', False), ('company_id', '=', company_id)]")
    writeoff_label = fields.Char(string='Journal Item Label', default='Write-Off',
        help='Change label of the counterpart that will hold the payment difference')

    def post(self):
        for rec in self:
            payments = rec.payment_lines_ids
            payments.action_post()
            # TODO add payable accounts also to get both of them
            move_lines = payments.mapped('line_ids').filtered(lambda r: not r.reconciled and r.account_id.reconcile and r.account_internal_type == 'receivable') + rec.move_line_ids.filtered(lambda r: not r.reconciled and r.account_id.reconcile and r.account_internal_type == 'receivable')
            move_lines.reconcile()
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
            ('account_id.internal_type', '=', 'receivable'),
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
