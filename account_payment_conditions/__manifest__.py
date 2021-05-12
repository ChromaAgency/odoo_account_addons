# -*- coding: utf-8 -*-
{
    'name': "Condiciones de pago",

    'summary': """
    Modulo para agregar condiciones de pago 
    """,

    'description': """
    Modulo para agregar condiciones de pago


    """,

    'author': "Making Argentina",
    'website': "https://making.com.ar",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Account',
    'version': '0.1',
    'installable': True,
    # any module necessary for this one to work correctly
    'depends': ['account', 'sale'],
    # always loaded
    'data': [
        'views/views.xml',
        'security/ir.model.access.csv',
    ]
}
