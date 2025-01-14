from odoo.fields import Many2many, Date
from odoo.models import Model
from odoo.api import onchange
import logging
_logger = logging.getLogger(__name__)
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

    def get_witholding_dict(self, subtotal, withholding, withholdings_dict):
        today = Date.context_today(self)
        old_moves = self.env['account.move.line'].search([
        ('partner_id.commercial_partner_id', '=', self.partner_id.commercial_partner_id.id),
        ('move_id.state', '=', 'posted'),
        ('date', '<', today ),
        ('date', '>=', today.replace(day=1)),
        ('product_withholding_ids', '=', withholding.id),
        ('id', '!=', self.id),
        ])
        # This has to change
        old_subtotal = 0 # sum(old_moves.mapped('price_subtotal'))
        withholdings_amount = withholdings_dict.get(withholding.id, {}) 
        base_amount = withholdings_amount.get("base_amount",0)
        new_base_amount = subtotal - max(withholding.untaxed_amount - old_subtotal, 0)
        base_amount_to_withhold, percentage_int, excedent_fraction = withholding.get_withholding_amount(new_base_amount)
        new_amount = base_amount_to_withhold + ((new_base_amount - excedent_fraction) * percentage_int )
        amount = withholdings_amount.get("amount",0) + new_amount
        return {
                    "amount":amount,
                    "base_amount":base_amount + new_base_amount,
                }

    def get_withholdings_amount(self):
        withholdings_dict = {}
        for rec in self:
            withholdings = rec.product_withholding_ids
            subtotal = rec.price_subtotal
            for withholding in withholdings:
                withholdings_dict.update({withholding.id: rec.get_witholding_dict(subtotal, withholding, withholdings_dict)})
        return withholdings_dict  