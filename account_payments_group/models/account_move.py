# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.fields import Integer, One2many, Many2many, Many2one, Date, Float, Char, Text, Selection
from odoo.api import depends, onchange, returns
from odoo.models import Model
from odoo.exceptions import UserError
import logging
_logger = logging.getLogger(__name__)


class AccountMove(Model):
    _inherit = 'account.move'

    payment_group_ids = Many2many('account.payment.group',string="Grupos de pagos", compute="_compute_payment_group_ids")
    payment_group_count = Integer(string="Pagos", compute="_compute_payment_group_ids")

    def open_payment_groups(self):
        payment_group_data = {
            'name': _('Grupos de pagos'),
            'res_model': 'account.payment.group',
            'view_mode': 'list,form',
            'context': self.env.context,
            'target': 'current',
            'domain': [('id','in',self.payment_group_ids.ids)],
            'type': 'ir.actions.act_window',
        }
        return payment_group_data
    
    def action_register_payment(self):
        ctx = self.env.context.copy()
        active_ids = self.ids
        if not active_ids:
            raise UserError('Por alguna razon el emisor/receptor del pago no pudo ser determinado')
        invoices = self.env['account.move'].browse(active_ids).filtered(lambda move: move.is_invoice(include_receipts=True))
        # TODO We should change this to be able to identify is we have to pay more than receive or viceversa
        default_payment_type = 'receivable'
        if any(invoice.move_type == 'in_invoice' for invoice in invoices):
            default_payment_type = 'payable'
        ctx.update({
            'default_partner_id':invoices[0].commercial_partner_id.id,
            'active_ids':False,
            'active_id':False,
            'active_model':False,
            'default_payment_type':default_payment_type,
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
        #hello = 'hello'
        for rec in self:
            payment_groups2 = self.env['account.payment.group'].search([]).move_line_ids
            payment_groups = self.env['account.payment.group'].search([('move_line_ids','in',rec.line_ids.ids)]).ids
            _logger.info('rec line ids: %s', rec.line_ids.ids)
            _logger.info('esto hay en payment groups %s',payment_groups2)
            _logger.info('Payment groups tiene contenido? %s', payment_groups)
            rec.payment_group_ids = payment_groups
            rec.payment_group_count = len(payment_groups)

