# -*- coding: utf-8 -*-
{
    'name': "Addons para cheques",

    'summary': """
    Modulo para cheques
    """,

    'description': """
    Modulo para cheques
    """,

    'author': "Making Argentina",
    'website': "https://making.com.ar",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Localization',
    'version': '0.1',
    'installable': True,
    # any module necessary for this one to work correctly
    'depends': ['account'],
    # always loaded
    'data': [
       'views/views.xml',
        #'data/data.xml',

    ]
}
