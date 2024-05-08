# -*- coding: utf-8 -*-
from lxml import etree
from odoo import _, api, fields, models
from odoo.exceptions import UserError
import logging
_logger = logging.getLogger(__name__)
from dateutil.relativedelta import relativedelta

class AccountBankStatementLine(models.Model):
    _inherit = 'account.bank.statement.line'


    def _action_open_bank_reconciliation_widget(self, extra_domain=None, default_context=None, name=None, kanban_first=True):
        action = super(AccountBankStatementLine, self)._action_open_bank_reconciliation_widget(extra_domain=extra_domain, default_context=default_context, name=name, kanban_first=kanban_first)
        journal = self.env['account.journal'].browse(action['context']['default_journal_id'])
        if journal.block_journal_visibility:
            if self.env.user.has_group('accounting_advanced_security.cannot_read_journal'):                
                raise UserError(_('No tiene permisos para abrir este diario'))
        return action
