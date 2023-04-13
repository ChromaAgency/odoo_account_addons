from odoo import models, fields
from odoo.fields import Many2one, Many2many

class ResPartner(models.Model):
    _inherit = "res.partner"

    group_ids = Many2many('res.groups', 'res_partner_group_rel', 'partner_id', 'group_id', string='Groups')
