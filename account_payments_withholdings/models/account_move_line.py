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
            # TODO Should this be price subtotal?
            subtotal = rec.price_subtotal
            for withholding in withholdings:
                #TODO should manager all the possibilities (check if amount tax has a function to calculate this.)
                withholdings_amount = withholdings_dict.get(withholding.id, {}) 
                amount = withholdings_amount.get("amount",0) + (subtotal * (withholding.amount / 100))
                base_amount = withholdings_amount.get("base_amount",0) + subtotal
                withholdings_dict.update({withholding.id: {
                    "amount":amount,
                    "base_amount":base_amount,
                }})
        return withholdings_dict  