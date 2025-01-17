from odoo import models, fields

class ResPartner(models.Model):
    _inherit = 'res.partner'

    withholding_group = fields.Char(string='Withholding Group')