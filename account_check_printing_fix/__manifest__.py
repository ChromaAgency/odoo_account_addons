# -*- coding: utf-8 -*-
{
    'name': "Fix account check printing",

    'summary': """
        Modulo para evitar los issues que tiene el modulo de cheques
    """,

    'description': """    """,

    'author': "Chroma",
    'website': "https://portal.chroma.agency/",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Account',
    'version': '17.0.1.0',
    'installable': True,
    # any module necessary for this one to work correctly
    'depends': ['account_check_printing'],
    # always loaded
    'data': [
    
    ]
}
