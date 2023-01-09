from odoo.fields import  Date
from odoo.models import Model
from odoo import api
import logging

_logger = logging.getLogger(__name__)

class res_currency_rate(Model):
    _inherit = 'res.currency.rate'


    @api.model
    def create(self, vals_list):
        records = super().create(vals_list)
        records.update_the_other_company()
        return records


    def update_the_other_company(self):
        this_company = self.company_id
        all_companies = self.env['res.company'].sudo().search([('currency_id','=', this_company.currency_id.id),('id', '!=', this_company.id)])
       
        for company in all_companies:
            last_other_company_currency_rate = company.env['res.currency.rate'].sudo().search([('name', '=', Date.today()),('company_id', 'in', company.ids)])
            if not last_other_company_currency_rate:
                self.sudo().create([{
                    'name': self.name,
                    'rate': self.rate,
                    'currency_id' : self.currency_id.id,
                    'company_id' : company.id
                }])