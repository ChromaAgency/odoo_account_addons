# -*- coding: utf-8 -*-
from odoo.models import Model, TransientModel, AbstractModel
from odoo.fields import Char,Float,Many2one
from odoo.exceptions import UserError
class CurrencyConversion(AbstractModel):
  _name="res.currency.conversion"
  _description = "This model works as a wizard to make currency conversions easy to the users"

  company_id = Many2one('res.company', default=lambda s:s.env.company)
  company_currency_id = Many2one('res.currency', related='company_id.currency_id')
  source_currency = Many2one('res.currency',string="Moneda actual")
  target_currency = Many2one('res.currency',string="Moneda Destino")
  exchange_rate = Float(string="Tipo de cambio")

  def confirm(self):
    ctx = self._context
    active_ids = ctx.get('active_ids')
    if not active_ids:
      raise UserError('''
        No active Id
        No se pudo convertir la moneda en el documento actual ya que no encontramos información en que documento se estaba trabajando, esto puede deberse a un bug o que se esta intentando usar este formulario desde un lugar indebido.

        Información para el programador:
        ids: {active_ids}
      '''.format(active_ids=str(active_ids)))
  
class CurrencyConversionWizard(TransientModel):
  _name="res.currency.conversion.wizard"
  _inherit = "res.currency.conversion"

  def confirm(self):
    
class InvoiceCurrencyConversion(TransientModel):
  _name="res.currency.conversion.invoice.wizard"
  _inherit = "res.currency.conversion"
  
  def confirm(self):
    ctx = self._context
    active_ids = ctx.get('active_ids')
    account_moves = self.env['account.move'].browse(active_ids)
    for am in account_moves:
      for aml in am.invoice_line_ids:
        aml.price_unit * self.exchange_rate



