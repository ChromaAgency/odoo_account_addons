# -*- coding: utf-8 -*-
from odoo.api import model,constrains, onchange, depends
from odoo.models import Model
from odoo.fields import Many2many, Many2one,Char, Integer, Selection
from odoo.exceptions import ValidationError
from num2words import num2words
import logging
_logger = logging.getLogger(__name__)

class AccountPaymentGroup(Model):
    _inherit = 'account.payment.group'
    
    sequence_id = Many2one(related="receipt_book_id.sequence_id", string="Secuencia")
    receipt_book_id = Many2one("account.payment.receipt_book", string="Talonario de recibos", required=True)
    payment_total_in_letters = Char('Recibimos')

    @onchange('partner_id')
    def _onchange_payment_type(self):
        for rec in self:
            current_company = self.env.company
            receipt_book = self.env['account.payment.receipt_book'].search([
                ('payment_type', '=', rec.payment_type),
                ('company_id', '=', current_company.id)
            ], limit=1)
            rec.receipt_book_id = receipt_book.id
            
    @model
    def create(self, vals_list):
        for rec in self:
            rec.receipt_book_id._check_next_sequence_number()
        return super(AccountPaymentGroup,self).create(vals_list)
    
    @onchange('payments_total')
    def convert_to_letters(self):
        for rec in self:
            converted_number = num2words(rec.payments_total, lang='es', to='currency')

            if 'euros' in converted_number:
                converted_number = converted_number.replace('euros', 'pesos')
            
            if 'céntimos' in converted_number:
                converted_number = converted_number.replace('céntimos', 'centavos')

            rec.payment_total_in_letters = converted_number

class ReceiptBook(Model):
    _name = "account.payment.receipt_book"
    _description = "Talonarios de recibo"

    company_id = Many2one('res.company', string="Compañía")
    sequence_id = Many2one('ir.sequence',string="Secuencia", required=True, default=lambda self:self.env.ref('account_payments_group.ir_sequence_account_payments_group'))
    name = Char(string="Nombre", required=True)
    payment_type = Selection([('receivable','Recibo'),('payable','Orden de pago')], string="Tipo de pago", required=True)
    lowest_number = Integer('Primer Número', required=True)
    highest_number = Integer('Último Número', required=True)

    def _check_next_sequence_number(self):
        for rec in self:
            next_sequence_number = rec.sequence_id.number_next_actual
            if next_sequence_number > rec.highest_number or next_sequence_number < rec.lowest_number:
                raise ValidationError('Este talonario ya se uso completamente, por favor utilice uno distinto'
            'El número siguiente era {}'.format(next_sequence_number) 
            )

class AccountMove(Model):
    _inherit = 'account.move'

    invoiced_amount_in_letters = Char(string='Facturación en letras')
    stock_picking_ids = Many2many('stock.picking','account_move_voucher_relation','account_move_id','stock_picking_id',string="Remito/s de esta factura")

    def get_related_stock_pickings(self):
        """ Get and prepare data to show a table of invoiced lot on the invoice's report. """
        self.ensure_one()

        if self.state == 'draft':
            return []

        return self.stock_picking_ids.mapped('voucher_ids.name')