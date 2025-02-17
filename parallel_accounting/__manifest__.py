# -*- coding: utf-8 -*-
{
    'name': "Contabilidad Cuentas contables alternativas",

    'summary': "Permite la utilización de cuentas alternativas basadas en los diarios de contabilidad",

    'description': """
        A través del campo Usa documentos, permite asignar una cuenta u otra a la contabilidad de la empresa
    """,

    'author': "Chroma",
    'website': "https://chroma.agency",

    'category': 'Accounting',
    'version': '0.1',

    'depends': ['base', 'account'],

    'data': [
        'views/product_template_views.xml',
        'views/res_partner_views.xml',
    ],
    'demo': [
        'demo/demo.xml',
    ],
}

