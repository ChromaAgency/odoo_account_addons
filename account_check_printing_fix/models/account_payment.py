from odoo import api, fields, models, _

class AccountPayment(models.Model):
    _inherit = "account.payment"
    
    @api.constrains('check_number', 'journal_id')
    def _constrains_check_number(self):
        checks = self.filtered(lambda x: x.payment_method_line_id.code == 'check_printing')
        return super(AccountPayment, self - checks)._constrains_check_number()