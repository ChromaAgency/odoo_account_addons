# -*- coding: utf-8 -*-
{
    'name': "Condiciones de pago en RMA",

    'summary': """
    Modulo para agregar condiciones de pago en RMA
    """,

    'description': """
    Modulo para agregar condiciones de pago en RMA


    """,

    'author': "Chroma",
    'website': "https://portal.chroma.agency/",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Account',
    'version': '0.1',
    'installable': True,
    # any module necessary for this one to work correctly
    'depends': ['account', 'repair', 'account_payment_conditions'],
    # always loaded
    'data': [
        'views/views.xml',
        'reports/repair_order2.xml'
    ]
}
