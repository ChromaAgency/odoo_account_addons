# -*- coding: utf-8 -*-
{
    'name': "Account Sale Currency Invoicing",

    'summary': """
        Make the invoice in a different currency than the order currency
            """,

    'description': """
        Make the invoice in a different currency than the order currency.
        

    """,

    'author': "Chroma",
    'website': "https://portal.chroma.agency/",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Sales',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','sale_management','account'],
    'data': [
            'views/res_partner.xml',
            'views/sale_order.xml'
    ]
}
