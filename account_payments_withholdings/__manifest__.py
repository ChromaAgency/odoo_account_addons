# -*- coding: utf-8 -*-
{
    'name': "Retenciones en Pagos",

    'summary': """
    Modulo para adaptar las retenciones a pagos
    """,

    'description': """
    Modulo para adaptar las retenciones a pagos
    """,

    'author': "Chroma",
    'website': "https://portal.chroma.agency/",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Localization',
    'version': '17.0.1',
    'installable': True,
    # any module necessary for this one to work correctly
    'depends': ['account'],
    # always loaded
    'data': [
       'views/account_move.xml',
       'data/data.xml',
       'data/ir.sequence.xml',
       'views/account_payment.xml',
       'views/account_tax.xml',
       'views/product_template.xml',

    ]
}
