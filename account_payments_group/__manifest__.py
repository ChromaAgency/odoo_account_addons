# -*- coding: utf-8 -*-
{
    'name': "Metodos de pago agrupados",

    'summary': """
    Modulo para crear pagos con diferentes metodos de pago, y agruparlos en una sola vista
    """,

    'description': """
    Modulo para crear pagos con diferentes metodos de pago, y agruparlos en una sola vista
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
    'depends': ['account','l10n_latam_check','account_payments_withholdings'],
    # always loaded
    'data': [
        'views/views.xml',
        'security/ir.model.access.csv',
        'data/ir.sequence.xml',
        'data/ir.actions.xml',
        'data/ir.menu.xml',
        'reports/reports.xml',
    ]
}
