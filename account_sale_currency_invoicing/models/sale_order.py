from odoo.exceptions import UserError
from odoo import api, fields, models, _
from odoo.fields import Date, Many2one
from odoo.api import onchange
import logging
_logger=logging.getLogger(__name__)
class SaleOrder(models.Model):
    _inherit = "sale.order"
    
    invoicing_currency = Many2one('res.currency',string='Moneda para facturar')

    @onchange('partner_id')
    def _onchange_partner_id_invoicing_currency(self):
        for rec in self:
            # TODO Check if this works with commercial partner
            rec.invoicing_currency = rec.partner_id.invoicing_currency


    def _prepare_invoice(self):
        """
        Prepare the dict of values to create the new invoice for a sales order. This method may be
        overridden to implement custom invoice generation (making sure to call super() to establish
        a clean extension chain).
        """
        self.ensure_one()
        invoice_vals = super()._prepare_invoice()
        invoice_vals.update({
            'currency_id': self.invoicing_currency.id,
        })
        return invoice_vals

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    def _prepare_invoice_line(self, **optional_values):
        """
        Prepare the dict of values to create the new invoice line for a sales order line.

        :param qty: float quantity to invoice
        :param optional_values: any parameter that should be added to the returned invoice line
        """
        self.ensure_one()
        res = super()._prepare_invoice_line(**optional_values)
        if self.order_id.currency_id.id!=self.order_id.invoicing_currency.id:
            res.update({
                'price_unit': self.order_id.currency_id._convert(self.price_unit, self.order_id.invoicing_currency, self.env.company, Date.today())
            })
        return res