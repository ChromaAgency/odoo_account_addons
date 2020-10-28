# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.fields import One2many, Many2many,Many2one,Date,Float,Char,Text,Selection
from odoo.api import depends,onchange,returns
from odoo.models import Model
from odoo.exceptions import UserError

class AccountPayment(Model):
    _inherit = 'account.payment'
    
    payment_group_id = Many2one('account.payment.group', string="Payment Group")
class PaymentGroup(Model):
    _name = 'account.payment.group'
    _description = 'Groups different lines of account.payment and relates them with account.move lines (invoices, and other)'
    _inherit = 'mail.thread'
    _order = "payment_date desc"
    
    name = Char(string="Nombre")
    sequence_id = Many2one('ir.sequence',string="Secuencia")
    state = Selection([('draft','Borrador'),('posted','Validado'),('canceled','Cancelado')],default="draft", string="Estado")
    payment_lines_ids = One2many('account.payment','payment_group_id', string="Pagos")
    move_ids = Many2many('account.move',string="Movimientos imputados", states={'posted':[('readonly',True)]}) 
    company_id = Many2one('res.company',string="Compañia")
    partner_id = Many2one('res.partner', string="Contacto")
    payment_date = Date(string='Fecha de pago')
    observations = Text(string='Observaciones')
    payments_total = Float(string="Monto pago",compute="_compute_payments_total")
    unpaid_amount = Float(string="Monto adeudado",compute="_onchange_partner_id")
    matched_amount = Float(string="Importe imputado", compute="_compute_matched_amount")
    unmatched_amount = Float(string="Importe no imputado", compute="_compute_matched_amount")

    def post(self):
        for rec in self:
            for move_ids in rec.move_ids:
                continue
            rec.state = 'posted'

    def cancel(self):
        for rec in self:
            rec.state = 'canceled'
    
    def to_draft(self):
        for rec in self:
            rec.state = 'draft'

    @returns('account.move')
    def _get_unconcilied_move_ids(self):
        account_moves = self.env['account.move'].search([('partner_id','=',self.partner_id.id),('amount_residual','>',0),('state','=','posted')])
        return account_moves

    def add_all_moves(self):
        for rec in self:
            move_ids = rec._get_unconcilied_move_ids().ids
            rec.move_ids = [(6,0,move_ids)]

    @onchange('partner_id')
    def _onchange_partner_id(self):
        for rec in self:
            if rec.partner_id:
                rec.unpaid_amount = sum(rec.partner_id.invoice_ids.mapped('amount_residual'))
                rec.move_ids = False
                rec.payment_lines_ids = False
    @depends('payment_lines_ids')
    def _compute_payments_total(self):
        for rec in self:
            rec.payments_total = sum(rec.payment_lines_ids.mapped('amount'))
    @depends('payments_total','move_ids')
    def _compute_matched_amount(self):
        for rec in self:
            amount_residual = sum(rec.move_ids.mapped('amount_residual'))
            payments = rec.payments_total
            matched_amount = payments if payments <= amount_residual else amount_residual
            rec.matched_amount = matched_amount
            rec.unmatched_amount = amount_residual - payments  if amount_residual > 0 else 0
