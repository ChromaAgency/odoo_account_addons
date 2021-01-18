# -*- coding: utf-8 -*-
{
    'name': "Selector de precios",

    'summary': """
    Modulo para realizar cambios en la lista de precios en la vista de facturas 
    """,

    'description': """
    Modulo para realizar cambios la vista de las facturas de manera rapida
    
    Historias de usuario que motivan a este modulo:

    Como administrativo quiero poder definir los precios en el momento exacto antes de facturar


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
    'depends': ['account'],
    # always loaded
    'data': [
        'views/views.xml',
    ]
}
