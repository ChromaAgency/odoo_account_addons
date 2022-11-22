# -*- coding: utf-8 -*-
from datetime import datetime
from odoo.api import Environment
from odoo.tests.common import TransactionCase, Form, tagged
from logging import getLogger

_logger = getLogger(__name__)

filter_invoices = lambda r: r.account_id.reconcile and r.account_internal_type == 'receivable'

@tagged('post_install', '-at_install')
class TestAccountPaymentGroup(TransactionCase):
    
    def _create_usd_move_lines(self, currency_id, partner_id):
        balance = -10
        debt_account_id = self.env.ref('l10n_ar.1_base_deudores_por_ventas').id
        write_off_account_id = self.env.ref('l10n_ar.1_base_venta_de_mercaderia').id
        tax_id = self.env.ref('l10n_ar.1_ri_tax_vat_21_ventas').id
        return [
                (0,0,{
                    'name': "test deby",
                'amount_currency': -balance,
                'currency_id': currency_id,
                'debit': -balance if balance < 0.0 else 0.0,
                'credit': balance if balance > 0.0 else 0.0,
                'partner_id': partner_id,
                'account_id': debt_account_id,
                'tax_ids':[(4,tax_id)]
                }),
                (0,0,{
                'name': "test ingre",
                'amount_currency': balance,
                'currency_id': currency_id,
                'debit': balance if balance > 0.0 else 0.0,
                'credit': -balance if balance < 0.0 else 0.0,
                'partner_id': partner_id,
                'account_id': write_off_account_id,
                'tax_ids':[(4,tax_id)]
            })]

    def _create_invoice(self, journal_id, currency_id, partner_id):
        return self.env['account.move'].create([{
            'partner_id':partner_id,
            'journal_id':journal_id,
            'currency_id':currency_id,
            'line_ids': self._create_usd_move_lines(currency_id, partner_id),
            'l10n_latam_document_type_id':self.env.ref('l10n_ar.dc_a_f').id,
            'move_type':'out_invoice'
        }])
        
    def _create_invoices(self):
        env = self.env 
        USD = env.ref('base.USD').id
        ARS = env.ref('base.ARS').id
        env.ref('base.USD').rate_ids = [(0,0,{
            'name':datetime.today(),
            'rate':0.001,
            'company_id':self.env.company.id
        })]
        partner = env['res.partner'].create({
            'name':"test 1"
        })
        partner2 = env['res.partner'].create({
            'name':"test 2"
        })
        self.usd_invoice = self._create_invoice(1, USD, partner.id)
        self.usd_invoice.action_post()
        self.ars_invoice = self._create_invoice(1, ARS, partner2.id)
        self.ars_invoice.action_post()
        env.ref('base.USD').rate_ids.write({
            'rate':0.0009
        })

    def setUp(self):
        super_return =  super().setUp()
        self.env: Environment
        self._create_invoices()
        return super_return
    
    def _create_payment_line(self, pg_form, amount):
        journal = self.env['account.journal'].search([('type','=','bank')], limit=1)
        with pg_form.payment_lines_ids.new() as payment:
            payment.ref = 'Test'
            payment.amount = amount
            payment.journal_id = journal
            payment.payment_type = 'inbound'
            payment.payment_method_id = payment.journal_id.inbound_payment_method_ids[:1]
            

    def test_01_usd_invoice_1_payment(self):
        partner_id = self.usd_invoice.partner_id.id
                
        with Form(self.env['account.payment.group'].with_context(default_partner_id=partner_id)) as pg_form:
            pg_form.writeoff_journal_id = self.env['account.journal'].search([('type','=','general')], limit=1)
            pg_form.writeoff_account_id = self.env.ref('l10n_ar.1_base_diferencias_de_cambio')
            self._create_payment_line(pg_form, 10)
        payment_g = pg_form.save()
        payment_g.post()
        residual_amount = sum(self.usd_invoice.line_ids.filtered(filter_invoices).mapped('amount_residual'))
        self.assertEqual(residual_amount, 0)
    
    def test_02_usd_invoice_multi_payment(self):
        partner_id = self.usd_invoice.partner_id.id
                
        with Form(self.env['account.payment.group'].with_context(default_partner_id=partner_id)) as pg_form:
            pg_form.writeoff_journal_id = self.env['account.journal'].search([('type','=','general')], limit=1)
            pg_form.writeoff_account_id = self.env.ref('l10n_ar.1_base_diferencias_de_cambio')
            self._create_payment_line(pg_form, 5)
        payment_g = pg_form.save()
        payment_g.post()
        residual_amount = sum(self.usd_invoice.line_ids.filtered(filter_invoices).mapped('amount_residual'))
        self.assertEqual(residual_amount, 5)
        with Form(self.env['account.payment.group'].with_context(default_partner_id=partner_id)) as pg_form:
            pg_form.writeoff_journal_id = self.env['account.journal'].search([('type','=','general')], limit=1)
            pg_form.writeoff_account_id = self.env.ref('l10n_ar.1_base_diferencias_de_cambio')
            self._create_payment_line(pg_form, 5)
        payment_g = pg_form.save()
        payment_g.post()
        residual_amount = sum(self.usd_invoice.line_ids.filtered(filter_invoices).mapped('amount_residual'))

        self.assertEqual(residual_amount, 0)

    def test_03_ars_invoice_1_payment(self):
        partner_id = self.ars_invoice.partner_id.id
                
        with Form(self.env['account.payment.group'].with_context(default_partner_id=partner_id)) as pg_form:
            pg_form.writeoff_journal_id = self.env['account.journal'].search([('type','=','general')], limit=1)
            pg_form.writeoff_account_id = self.env.ref('l10n_ar.1_base_diferencias_de_cambio')
            self._create_payment_line(pg_form, 10)
        payment_g = pg_form.save()
        payment_g.post()
        residual_amount = sum(self.ars_invoice.line_ids.filtered(filter_invoices).mapped('amount_residual'))
        self.assertEqual(residual_amount, 0)


    def test_04_ars_invoice_multi_payment(self):
        partner_id = self.ars_invoice.partner_id.id
                
        with Form(self.env['account.payment.group'].with_context(default_partner_id=partner_id)) as pg_form:
            pg_form.writeoff_journal_id = self.env['account.journal'].search([('type','=','general')], limit=1)
            pg_form.writeoff_account_id = self.env.ref('l10n_ar.1_base_diferencias_de_cambio')
            self._create_payment_line(pg_form, 5)
        payment_g = pg_form.save()
        payment_g.post()
        residual_amount = sum(self.ars_invoice.line_ids.filtered(filter_invoices).mapped('amount_residual'))
        self.assertEqual(residual_amount, 5)
        with Form(self.env['account.payment.group'].with_context(default_partner_id=partner_id)) as pg_form:
            pg_form.writeoff_journal_id = self.env['account.journal'].search([('type','=','general')], limit=1)
            pg_form.writeoff_account_id = self.env.ref('l10n_ar.1_base_diferencias_de_cambio')
            self._create_payment_line(pg_form, 5)
        payment_g = pg_form.save()
        payment_g.post()
        residual_amount = sum(self.ars_invoice.line_ids.filtered(filter_invoices).mapped('amount_residual'))
        self.assertEqual(residual_amount, 0)

    def test_05_ars_invoice_1_payment_incomplete_close(self):
        partner_id = self.usd_invoice.partner_id.id
                
        with Form(self.env['account.payment.group'].with_context(default_partner_id=partner_id)) as pg_form:
            pg_form.writeoff_journal_id = self.env['account.journal'].search([('type','=','general')], limit=1)
            pg_form.writeoff_account_id = self.env.ref('l10n_ar.1_base_diferencias_de_cambio')
            pg_form.payment_difference_handling = 'reconcile'
            self._create_payment_line(pg_form, 5)
        payment_g = pg_form.save()
        payment_g.post()
        residual_amount = sum(self.usd_invoice.line_ids.filtered(filter_invoices).mapped('amount_residual'))
        self.assertEqual(residual_amount, 0)


    def test_06_ars_invoice_multi_payment_incomplete_close(self):
        partner_id = self.ars_invoice.partner_id.id
                
        with Form(self.env['account.payment.group'].with_context(default_partner_id=partner_id)) as pg_form:
            pg_form.writeoff_journal_id = self.env['account.journal'].search([('type','=','general')], limit=1)
            pg_form.writeoff_account_id = self.env.ref('l10n_ar.1_base_diferencias_de_cambio')
            pg_form.payment_difference_handling = 'reconcile'
            self._create_payment_line(pg_form, 5)
        payment_g = pg_form.save()
        payment_g.post()
        residual_amount = sum(self.ars_invoice.line_ids.filtered(filter_invoices).mapped('amount_residual'))
        self.assertEqual(residual_amount, 0)
