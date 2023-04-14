from odoo import models, fields
from odoo.fields import Many2one, Many2many

class AccountJournal(models.Model):
    _inherit = "account.journal"

    group_ids = Many2many('res.groups', 'account_journal_group_rel', 'journal_id', 'group_id', string='Groups')