# -*- coding: utf-8 -*-
from odoo.models import Model, TransientModel, AbstractModel
from odoo.fields import Char,Float,Many2one,Date
from odoo.exceptions import UserError
from odoo.api import onchange
from odoo.tools import float_is_zero
from odoo import _
import logging

_logger = logging.getLogger(__name__)
class CurrencyConversion(AbstractModel):
  _name="res.currency.conversion"
  _description = "This model works as a wizard to make currency conversions easy to the users"

  def get_exchange_rate(self):
    def exchange_rate_for(source_currency_rate):
      exchange_rate = 0
      if not float_is_zero(self.target_currency.rate, precision_rounding=self.target_currency.rounding or 0.00001) and not float_is_zero(source_currency_rate,precision_rounding=0.000001):
        exchange_rate = self.target_currency.rate/source_currency_rate
      return exchange_rate

    if(self.company_currency_id.id != self.source_currency.id):
      return exchange_rate_for(self.source_currency.rate)
    return exchange_rate_for(1)

  company_id = Many2one('res.company', default=lambda s:s.env.company)
  company_currency_id = Many2one('res.currency', related='company_id.currency_id')
  source_currency = Many2one('res.currency',string="Moneda actual",required=True,readonly=True)
  target_currency = Many2one('res.currency',string="Moneda Destino",required=True)
  exchange_rate = Float(string="Tipo de cambio",readonly=False,default=get_exchange_rate,digits=(100,10) )

  @onchange('target_currency')
  def _onchange_target_currency(self):
    _logger.info(self._context.get('active_ids'))
    self.exchange_rate = self.get_exchange_rate()

  def confirm(self):
    if(self.target_currency.id == self.source_currency.id):
      raise UserError(_('You should be converting a currency to a different currency'))
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

  def _currencies_to_change(self):
    """Responsibility: get the correct currencies to change"""
    currency = self.target_currency
    if( self.company_currency_id.id == self.source_currency.id):
      currency = self.target_currency
    if (self.company_currency_id.id == self.target_currency.id):
      currency = self.source_currency
    return currency

  def _get_updated_rate(self,currency):
    """Responsibility: create the correct rate for updating or creating a new rate id"""
    updated_rate = 0
    source_currency_id = self.source_currency.id
    currency_id = currency.id
    _logger.info(currency.name)
    if(currency_id != self.company_currency_id.id):
      if(source_currency_id != currency.id):
        updated_rate = target_currency_rate = self.source_currency.rate*self.exchange_rate
      else:
        if(not float_is_zero(self.exchange_rate,precision_rounding=currency.rounding or 0.00001)):
          updated_rate = source_currency_rate = self.target_currency.rate/self.exchange_rate
        else:
          raise UserError(_('Exchange rate cannot be 0'))
    else:
      updated_rate = 1
    return updated_rate
  def _currency_update_value(self,currency):
    today = Date.today()
    todays_rate = currency.rate_ids.filtered(lambda r: r.name == today)
    todays_rate_exists = bool(todays_rate)
    #TODO change this to represent the new rate
    updated_rate = self._get_updated_rate(currency)
    if(todays_rate_exists):
      update_value = [(1,todays_rate.id,{'rate':updated_rate})]
    else:
      update_value = [(0,0,{'rate':updated_rate,'name':today})]
    return update_value

  def _change_currency_rate_ids(self):
    """Responsibility: Change the rate in the currencies detected to change"""
    currencies = self._currencies_to_change()
    for currency in currencies:
      currency_rate_value = self._currency_update_value(currency)
      currency.rate_ids = currency_rate_value
      #Usa el exchange rate para el target

  def confirm(self):
    #si el tipo de cambio ARS/USD fuese 81.59 o USD/ARS = 0.012, 
    # el company_rate deberia ser 1/81.59 o 0.012, 
    # ahora si el tipo de cambio EUR/USD fuese 1.21 deberia dar  donde ARS/EUR = 0.010 | EUR/ARS = 98.77
    super(CurrencyConversionWizard,self).confirm()
    ctx = self._context
    if('update_company_exchange_rate' in ctx and ctx.get('update_company_exchange_rate')):
      _logger.info('changing_rate')
      self._change_currency_rate_ids()

    
class InvoiceCurrencyConversion(TransientModel):
  _name="res.currency.conversion.invoice.wizard"
  _inherit = "res.currency.conversion.wizard"
  
  def confirm(self):
    self.ensure_one()
    ctx = self._context
    active_ids = ctx.get('active_ids')
    account_moves = self.env['account.move'].browse(active_ids).with_context(check_move_validity=False)
    for am in account_moves:
      if am.state == 'posted':
        raise UserError(_('You cant change an already posted invoice'))
      message = _("Currency changed from %s to %s with rate %s") % (
              am.currency_id.name, self.target_currency.name,
              self.exchange_rate)
      for aml in am.line_ids:
        aml.price_unit = aml.price_unit * self.exchange_rate
      am.currency_id = self.target_currency.id
      am._onchange_currency()
      am.message_post(body=message)
      super(InvoiceCurrencyConversion,self).confirm()
    return {'type': 'ir.actions.act_window_close'}

class PaymentCurrencyConversion(TransientModel):
  _name="res.currency.conversion.payment.wizard"
  _inherit = "res.currency.conversion.wizard"
  
  def confirm(self):
    self.ensure_one()
    ctx = self._context
    active_ids = ctx.get('active_ids')
    # account_moves = self.env['account.move'].browse(active_ids).with_context(check_move_validity=False)
    # for am in account_moves:
    #   if am.state == 'posted':
    #     raise UserError(_('You cant change an already posted invoice'))
    #   message = _("Currency changed from %s to %s with rate %s") % (
    #           am.currency_id.name, self.target_currency.name,
    #           self.exchange_rate)
    #   for aml in am.line_ids:
    #     _logger.info(aml.exclude_from_invoice_tab)
    #     aml.price_unit = aml.price_unit * self.exchange_rate
    #   am.currency_id = self.target_currency.id
    #   am._onchange_currency()
    #   am.message_post(body=message)
    #   super(InvoiceCurrencyConversion,self).confirm()
    return {'type': 'ir.actions.act_window_close'}


