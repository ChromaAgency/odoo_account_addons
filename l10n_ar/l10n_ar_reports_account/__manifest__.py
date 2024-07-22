# -*- coding: utf-8 -*-
{
    'name': "Argentinian Account Reports",

    'summary': """Customized reports using the qweb engine for Argentinian Localization Account Module""",

    'description': """
        Customized reports using the qweb engine for Argentinian Localization Acount Module
        Uses Adhoc 
        Changed:
            
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
    'depends': ['base', 'l10n_ar','account_payments_group','sale','purchase','stock','account_accountant', 'l10n_ar_stock'],
    # always loaded
    'data': [
        #'report/report_templates.xml',
        'report/report_invoice_document.xml',
        'report/custom_header.xml',
        'report/paper_invoice.xml',
        'report/account_payments_group_report.xml',
        'views/views.xml',
        'security/ir.model.access.csv',
        'data/ir.actions.xml',
        'data/ir.menu.xml',
    ]
}
