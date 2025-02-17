# -*- coding: utf-8 -*-
from odoo.models import Model
from odoo.fields import Many2one, Char, Boolean
from odoo import _, api
class ResPartner(Model):
    _inherit = 'res.partner'
    
    property_receivables_secondary_account_id = Many2one('account.account', string=_('Receivables Secondary Account Property'), 
        domain="[('account_type', '=', 'asset_receivable'), ('deprecated', '=', False)]",
    check_company=True, company_dependent=True)
    property_payables_secondary_account_id = Many2one('account.account', string=_('Payables Secondary Account Property'), 
        domain="[('account_type', '=', 'liability_payable'), ('deprecated', '=', False)]",
    
    check_company=True, company_dependent=True)


    @api.model
    def _commercial_fields(self):
        return super(ResPartner, self)._commercial_fields() + \
            ['property_receivables_secondary_account_id', 'property_payables_secondary_account_id']