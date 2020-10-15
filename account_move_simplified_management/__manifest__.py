# -*- coding: utf-8 -*-
{
    'name': "Caja Simplificada",

    'summary': """
    Modulo para simplificar gastos en caja
    """,

    'description': """
    Modulo para simplificar gastos en caja
    """,

    'author': "Making Argentina",
    'website': "https://making.com.ar",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Invoicing',
    'version': '0.1',
    'installable': True,
    # any module necessary for this one to work correctly
    'depends': ['account'],
    # always loaded
    'data': [
       'views/views.xml',
       'data/data.xml',
       'actions/actions.xml',
        'security/ir.model.access.csv',
       'actions/menus.xml'
    ]
}
