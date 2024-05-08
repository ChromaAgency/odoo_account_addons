from odoo import models, fields
from odoo.fields import Many2one, Many2many, Boolean

class AccountJournal(models.Model):
    _inherit = "account.journal"

    group_ids = Many2many('res.groups', 'account_journal_group_rel', 'journal_id', 'group_id', string='Groups')
    block_journal_visibility = Boolean(string="Bloquear la visibilidad de este diario")
    show_moves_only_to = Many2many('res.groups', 'account_journal_group_rel_hide_moves', 'journal_id', 'group_id', string='Mostrar movimientos solo a')