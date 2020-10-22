from odoo.models import Model
from odoo.fields import Date, Char, Many2one

class AccountPayment(Model):
    _inherit = 'account.payment'

    check_number = Char(string="Número de cheque")
    check_date = Date(string="Fecha de pago")
    issuing_bank = Many2one('res.partner.bank',string="Banco Emisor")