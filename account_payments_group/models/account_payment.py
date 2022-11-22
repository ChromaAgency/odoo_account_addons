# -*- coding: utf-8 -*-
from odoo import   _
from odoo.fields import   Many2one
from odoo.api import model
from odoo.models import Model

class AccountPayment(Model):
    _inherit = 'account.payment'
    
    payment_group_id = Many2one('account.payment.group', string="Payment Group")
    
    def _add_partner_id_to_vals(self, vals):
        if 'payment_group_id' not in vals or vals.get('partner_id' ):
            return vals
        partner_id = self.env['account.payment.group'].browse([vals.get('payment_group_id')]).partner_id.id
        vals.update({
            'partner_id':partner_id
        })
        return vals

    def _add_partner_id_from_group_id(self, vals_list):
        return [self._add_partner_id_to_vals(vals) for vals in vals_list] if isinstance(vals_list, list) else self._add_partner_id_to_vals(vals_list)

    @model
    def create(self, vals_list):
        self._add_partner_id_from_group_id(vals_list)
        return super().create(vals_list)
