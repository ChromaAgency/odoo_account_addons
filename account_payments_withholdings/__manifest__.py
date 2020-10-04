# -*- coding: utf-8 -*-
{
    'name': "Retenciones en Pagos",

    'summary': """
    Modulo para adaptar las retenciones a pagos
    """,

    'description': """
    Modulo para adaptar las retenciones a pagos
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
    'depends': [],
    # always loaded
    'data': [
        'report/report_templates.xml',
        'report/report_invoice_document.xml',
        'report/paper_format.xml',
        'report/ir_actions_report.xml',
        'report/custom_header.xml',
    ]
}
