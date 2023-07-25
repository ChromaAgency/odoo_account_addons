from odoo.exceptions import UserError
from odoo import api, fields, models, _
from odoo.fields import Date, Many2one
from odoo.api import onchange

class Repair(models.Model):
    _inherit = "repair.order"
    
    # TODO add to view
    invoicing_currency = Many2one('res.currency',string='Moneda para facturar')

    @onchange('partner_id')
    def _onchange_partner_id_invoicing_currency(self):
        for rec in self:
            # TODO Check if this works with commercial partner
            rec.invoicing_currency = rec.partner_id.invoicing_currency


    def _create_invoices(self, group=False):
        repair_invoice_dict = super()._create_invoices(group=group)
        for repair, invoice in repair_invoice_dict.items():
            account_move = self.env['account.move'].browse([invoice])
            account_move.write({
        'currency_id': self.invoicing_currency.id
        })
            for line in account_move.invoice_line_ids:
                line.write({
                    'currency_id': self.invoicing_currency.id,
                    'price_unit' : self.currency_id._convert(line.price_unit, self.invoicing_currency, self.env.company, Date.today()),
                    'debit':  self.currency_id._convert(line.debit, self.invoicing_currency, self.env.company, Date.today()),
                    'credit': self.currency_id._convert(line.credit, self.invoicing_currency, self.env.company, Date.today())
                })
        return repair_invoice_dict

