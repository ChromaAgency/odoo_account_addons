# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.fields import One2many, Many2many,Many2one,Date,Float,Char
from odoo.api import depends
class PaymentGroup(models.Model):
    _name = 'account.payment.group'
    _description = 'Groups different lines of account.payment and relates them with account.move lines (invoices, and other)'

    payment_lines_ids = One2many('account.payment','payment_group_id', string="Pagos")
    move_line_ids = Many2many('account.move',string="Movimientos imputados") 
    company_id = Many2one('res.company',string="Compañia")
    partner_id = Many2one('res.partner', string="Contacto")
    payment_date = Date(string='Fecha de pago')
    observations = Char(string='Observaciones')
    payments_total = Float(string="Total pagado", compute="_compute_payments_total")
    matched_amount = Float(string="Importe imputado", compute="_compute_matched_amount")
    unmatched_amount = Float(string="Importe no imputado", compute="_compute_matched_amount")

    def _compute_payments_total(self):
        for rec in self:
            rec.payments_total = sum(rec.payment_lines_ids.mapped('amount'))
    
    @depends('payments_total')
    def __compute_matched_amount(self)
        for rec in self:
            rec.matched_amount = rec.payments_total - sum(rec.move_line_ids.mapped('amount_residual'))
