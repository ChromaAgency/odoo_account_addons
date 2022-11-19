from odoo import _
from odoo.models import Model
from odoo.fields import Float

class SaleOrder(Model):
    _inherit = "sale.order"

    payment_group_count = Float(string="Cuenta de recibos", compute="_compute_payment_group_count")

    def open_payment_groups(self): 
        payment_group_ids = self.invoice_ids.payment_group_ids.ids
        return {
            'name': _('Grupos de pagos'),
            'res_model': 'account.payment.group',
            'view_mode': 'list,form',
            'context': self.env.context,
            'target': 'current',
            'domain': [('id','in',payment_group_ids)],
            'type': 'ir.actions.act_window',
        }

    def _compute_payment_group_count(self):
        for rec in self.sudo():
            rec.payment_group_count = len(rec.invoice_ids.payment_group_ids)