# -*- coding: utf-8 -*-
{
    'name': "Conversiones de tipo de cambio",

    'summary': """
    Modulo para realizar cambios en el tipo de cambio de manera facil en las vistas de pagos 
    """,

    'description': """
    Modulo para realizar cambios en el tipo de cambio de manera facil en las vistas de pagos 
    
    Historias de usuario que motivan a este modulo:

    Como administrativo quiero actualizar la moneda de mis facturas mientras cambio los valores de los precios para no tener que hacerlo manualmente si hace falta.

    Como administrativo quiero actualizar el tipo de cambio de una moneda especifica de manera facil y con los valores que uso habitualmente

    Como administrativo me gustaria actualizar la moneda de mis pagos en diferente moneda a la de la factura


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
        'wizard/currency_conversion_wizard.xml',
    ]
}
