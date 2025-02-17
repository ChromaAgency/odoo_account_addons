# -*- coding: utf-8 -*-
from odoo.models import Model
from odoo.fields import Many2one, Char, Boolean
from odoo import _
ACCOUNT_DOMAIN = "['&', ('deprecated', '=', False), ('account_type', 'not in', ('asset_receivable','liability_payable','asset_cash','liability_credit_card','off_balance'))]"

class ProductTemplate(Model):
    _inherit = 'product.template'
    
    property_income_secondary_account_id = Many2one('account.account', domain=ACCOUNT_DOMAIN, string=_('Income Secondary Account'), check_company=True, company_dependent=True)
    property_expenses_secondary_account_id = Many2one('account.account', domain=ACCOUNT_DOMAIN, string=_('Expenses Secondary Account'), check_company=True, company_dependent=True)
    
    def _get_product_accounts(self):
        prods_account = super()._get_product_accounts()
        if self.env.context.get('use_secondary_account', False):
            prods_account.update({
                'income':self.property_income_secondary_account_id or self.property_account_income_id or self.categ_id.property_account_income_categ_id,
                'expense':self.property_expenses_secondary_account_id or self.property_account_expense_id or self.categ_id.property_account_expense_categ_id
            })
        return prods_account