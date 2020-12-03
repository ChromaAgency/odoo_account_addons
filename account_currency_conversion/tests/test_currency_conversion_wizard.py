from odoo.tests import TransactionCase, tagged

class TestCurrencyConversion(TransactionCase):

  @tagged('-standard')
  def create_basic_currency_object(self):
    company = self.env.company
    ars = self.env.ref('base.ARS')
    company.write({
      'currency_id':ars.id
    })
    self.eur = self.env.ref('base.EUR')
    self.usd = self.env.ref('base.USD')

  def test_company_currency(self):
    #We make a first test to see if company currency is ok
    self.create_basic_currency_object()
    currency_id = self.env.company.currency_id
    self.assertEqual(currency_id.id,self.env.ref('base.ARS').id,'Company id is wrongly sets all tests will probably fail')

  def test_conversion_function(self):
    #We test the conversion function actually works in the transient model by passing 3 different conversions
    test_conversions = [
      {
        #1st test is to convert 1 Eur to 1.19 USD/EUR
        'source_currency':self.eur,
        'target_currency':self.usd,
        'exchange_rate':1.19,
      },
      {
        #2st test is to convert 1 USD to 81.31 ARS/USD
        'source_currency':self.usd,
        'target_currency':self.ars,
        'exchange_rate':81.31,
      },
      {
        #3rd test is to convert 1 EUR to ARS where 1 USD is  ARS/USD
        'source_currency':self.eur,
        'target_currency':self.ars,
        'exchange_rate':96.76,
      },
    ]
    currency_conversion = self.env['res.currency.conversion'].create({

    })
    pass
    # self.assertEqual()