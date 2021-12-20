# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.fields import Integer, One2many, Many2many,Many2one,Date,Float,Char,Text,Selection
from odoo.api import depends,onchange,returns
from odoo.models import Model
from odoo.exceptions import UserError
import logging
_logger = logging.getLogger(__name__)
class AccountMove(Model):
    _inherit = 'account.move'

    payment_group_ids = Many2many('account.payment.group',string="Grupos de pagos", compute="_compute_payment_group_ids")
    payment_group_count = Integer(string="Pagos", compute="_compute_payment_group_ids")

    def open_payment_groups(self):
        return  {
            'name': _('Grupos de pagos'),
            'res_model': 'account.payment.group',
            'view_mode': 'list,form',
            'context': self.env.context,
            'target': 'current',
            'domain': [('id','in',self.payment_group_ids.ids)],
            'type': 'ir.actions.act_window',
        }
    
    def action_register_payment(self):
        ctx = self.env.context.copy()
        active_ids = self.ids
        if not active_ids:
            raise UserError('Por alguna razon el emisor/receptor del pago no pudo ser determinado')
        invoices = self.env['account.move'].browse(active_ids).filtered(lambda move: move.is_invoice(include_receipts=True))
        if any([invoice.move_type == 'in_invoice' for invoice in invoices]):
            return super(AccountMove, self).action_register_payment()
        ctx.update({
            'default_partner_id':invoices[0].commercial_partner_id.id,
            'active_ids':False,
            'active_id':False,
            'active_model':False,
        })
        
        action = self.env.ref('account_payments_group.payments_group_window').sudo().read()[0]
        action.update({
            'view_mode': 'form',
            'context': ctx,
            'views':[(False,'form'),(False,'tree')]
        })
        return action

    @depends('state','invoice_payments_widget')
    def _compute_payment_group_ids(self):
        for rec in self:
            payment_groups = self.env['account.payment.group'].search([('move_line_ids','in',rec.line_ids.ids)]).ids
            rec.payment_group_ids = payment_groups
            rec.payment_group_count = len(payment_groups)


class AccountPayment(Model):
    _inherit = 'account.payment'
    
    payment_group_id = Many2one('account.payment.group', string="Payment Group")


    

class PaymentGroup(Model):
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

    def post(self):
        for rec in self:
            payments = rec.payment_lines_ids
            payments.action_post()
            _logger.info(payments.mapped('line_ids').read())
            move_lines = payments.mapped('line_ids').filtered(lambda r: not r.reconciled and r.account_id.reconcile and r.account_internal_type == 'receivable') + rec.move_line_ids
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
        account_moves = self.env['account.move.line'].search([('partner_id','=',self.partner_id.id),('move_id.state','=','posted'),'|',('amount_residual','!=',0),('amount_residual_currency', '!=', 0.0),('account_id.reconcile', '=', True),('reconciled', '=', False)])
        return account_moves
        

    def add_all_unreconcilied_moves(self):
        for rec in self:
            move_line_ids = rec._get_unconcilied_move_line_ids().ids
            rec.move_line_ids = [(6,0,move_line_ids)]

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
            unreconciled_partner_amls = self.env['account.move.line']\
                                        .search([
                                            ('reconciled', '=', False),
                                            ('account_id.deprecated', '=', False),
                                            ('account_id.internal_type', '=', 'receivable'),
                                            ('move_id.state', '=', 'posted'),
                                            ('partner_id','=',rec.partner_id.id)
                                            ])
            unpaid_amount = sum(unreconciled_partner_amls.mapped('amount_residual'))
            rec.unpaid_amount = unpaid_amount
            amls = rec.move_line_ids
            amount_residual = sum(amls.mapped('amount_residual'))
            rec.unmatched_amount = amount_residual
            payments = rec.payments_total
            balance = sum(amls.mapped('balance'))
            if rec.state == 'posted':
                matched_amount = rec.matched_amount
            else:
                matched_amount = payments if payments <= amount_residual else amount_residual
            rec.matched_amount = matched_amount
