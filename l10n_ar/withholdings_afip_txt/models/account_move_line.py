from odoo import _
from odoo.models import Model

class AccountPayment(Model):
    _inherit = 'account.payment'

    def _prepare_arciba_txt_line(self):
        self.ensure_one()
        

    def get_arciba_txt_lines(self):
        lines = []
        for rec in self:
            if not rec.tax_withholding_id:
                continue
            lines.append(rec._prepare_arciba_txt_line())
        return lines