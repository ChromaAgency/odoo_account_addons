from odoo.exceptions import UserError
from odoo import api, fields, models, _
from odoo.fields import Date, Many2one
from odoo.api import onchange
import logging

_logger = logging.getLogger(__name__)

class Repair(models.Model):
    _inherit = "repair.order"
    
    invoicing_currency = Many2one('res.currency',string='Moneda para facturar')

    @onchange('partner_id')
    def _onchange_partner_id_invoicing_currency(self):
        for rec in self:
            rec.invoicing_currency = rec.partner_id.invoicing_currency

    def action_create_sale_order(self):
        res = super().action_create_sale_order()
        sale_order_id = res['res_id']
        sale_order = self.env['sale.order'].browse([sale_order_id])
        for line in sale_order.order_line:
            line.write({
                'currency_id': self.invoicing_currency.id,
                'price_unit' : self.invoicing_currency._convert(line.price_unit, line.currency_id, self.env.company, Date.today()),
            })
        sale_order.write({
            'invoicing_currency': self.invoicing_currency.id,
            'currency_rate': self.invoicing_currency.id,
            'currency_id': self.invoicing_currency.id,
        })
        
        sale_order._compute_amounts()
        return res



