# -*- coding: utf-8 -*-
{
    'name': "Metodos de pago agrupados en ventas",

    'summary': """
    Relación con ventas de recibos
    """,

    'description': """
    Relación con ventas de recibos
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
    'depends': ['account_payments_group_sale'],
    # always loaded
    'data': [
        'views/views.xml',
       
    ]
}
