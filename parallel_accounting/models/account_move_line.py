from odoo.models import Model 
from odoo.fields import Many2one, Char, Boolean
import logging
_logger = logging.getLogger(__name__)


class AccountMoveLine(Model):
    _inherit = 'account.move.line'

    def _compute_account_id(self):
        use_secondary_account = not self.move_id.journal_id.l10n_latam_use_documents
        aml = super(AccountMoveLine, self.with_context(use_secondary_account=use_secondary_account))._compute_account_id()
        if use_secondary_account:
            # Inspired from original _compute_account_id from @odoo/addons/account/models/account_move_line.py 
            term_lines = self.filtered(lambda line: line.display_type == 'payment_term')
            
            for line in term_lines:
                account_type = 'asset_receivable' if line.move_id.is_sale_document(include_receipts=True) else 'liability_payable'
                move = line.move_id
                partner_account_id = move.with_company(move.company_id).commercial_partner_id['property_receivables_secondary_account_id' if account_type == 'asset_receivable' else 'property_payables_secondary_account_id'].id
                account_id = (
                    partner_account_id
                    or move.with_company(move.company_id).company_id.partner_id['property_receivables_secondary_account_id' if account_type == 'asset_receivable' else 'property_payables_secondary_account_id'].id
                    # or move.with_company(move.company_id).commercial_partner_id['property_account_receivable_id' if account_type == 'asset_receivable' else 'property_account_payable_id'].id
                    # or move.with_company(move.company_id).company_id.partner_id['property_account_receivable_id' if account_type == 'asset_receivable' else 'property_account_payable_id'].id
                )
                if line.move_id.fiscal_position_id:
                    account_id = line.move_id.fiscal_position_id.map_account(self.env['account.account'].browse(account_id))
                line.account_id = account_id
        return aml