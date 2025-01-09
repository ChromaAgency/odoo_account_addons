from odoo.fields import Many2many
from odoo.models import Model
from odoo.api import onchange

class AccountMoveLine(Model):
    _inherit= "account.move.line"

    def default_get(self, fields_list):
        values = super().default_get(fields_list)
        product_id = values.get("product_id")
        if product_id:
            product = self.env["product.product"].browse(product_id)
            values["product_withholding_ids"] = product.product_withholding_ids.ids
        return values
    
    product_withholding_ids = Many2many('account.tax', 'withholding_account_move_line_account_tax_rel', 'account_move_line_id', 'account_tax_id', string= "Retenciones aplicables")
    
    @onchange('product_id')
    def _onchange_product_id_account_withholdings(self):
        self.product_withholding_ids = self.product_id.product_withholding_ids

    def get_withholdings_amount(self):
        withholdings_dict = {}
        for rec in self:
            withholdings = rec.product_withholding_ids
            old_moves = self.env['account.move.line'].search([
                ('partner_id.commercial_partner_id', '=', rec.partner_id.commercial_partner_id.id),
                ('move_id.state', '=', 'posted'),
                ('date', '<', rec.date),
                ('id', '!=', rec.id),
            ])
            old_subtotal = sum(old_moves.mapped('price_subtotal'))
            subtotal = rec.price_subtotal
            for withholding in withholdings:
                withholdings_amount = withholdings_dict.get(withholding.id, {}) 
                base_amount = withholdings_amount.get("base_amount",0)
                base_amount = subtotal - (min(old_subtotal, base_amount) - base_amount) 
                amount = withholdings_amount.get("amount",0) + (base_amount * (withholding.amount / 100))
                withholdings_dict.update({withholding.id: {
                    "amount":amount,
                    "base_amount":base_amount,
                }})
        return withholdings_dict  