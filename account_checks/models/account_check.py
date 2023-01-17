from email.policy import default
from tkinter import EW
from numpy import require
from odoo.models import Model
from odoo.fields import Date, Char, Many2one, Datetime, Selection, Monetary, One2many

class AccountPayment(Model):
    _name = 'account.check'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = Char(string="Numero", required=True)
    deposit_date = Datetime(string="Fecha de pago", required=True, default=Datetime.now)
    date = Datetime(string="Fecha de emision", required=True, default=Datetime.now)
    issuing_bank = Many2one('res.bank',string="Banco Emisor", required=True)
    partner_id = Many2one('res.partner', string="Emisor", required=True)
    state = Selection([
        ('in_hand', 'En Mano'),
        ('deposited', 'Depositado'),
        ('delivered', 'Entregado'),
        ('rejected', 'Rechazado'),
        ('returned', 'Devuelto'),
    ],
        required=True,
        default='in_hand',
    )
    amount = Monetary(string="Monto", currency_field="currency_id", required=True)
    amount_company_currency = Monetary(string="Monto en moneda de la compañia",
        currency_field="company_currency_id",
        compute="_compute_amount_company_currency"
    )
    company_id = Many2one("res.company",string="Compañia")
    currency_id = Many2one(
        'res.currency',
        default=lambda self: self.env.user.company_id.currency_id.id,
        required=True,
    )
    company_currency_id = Many2one(
        related='company_id.currency_id',
        string='Moneda de la empresa',
    )
    

    def action_return_check(self): ...
        # ? This should make a payment back to the original owner
    def action_deposit_check(self): ...
        # ? Thios should make an internal transfer from this model to the bank
    def action_deliver_check(self): ...
        # ? This should make a payment from us to a different contact
    def action_reject_check(self): ... 
        # ? This should make the internal transfer from the bank to us.

    def _compute_amount_company_currency(self):
        for rec in self:
            # TODO Compute with currency into the actual amount
            rec.amount_company_currency = rec.amount
