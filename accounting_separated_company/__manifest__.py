# -*- coding: utf-8 -*-
{
    'name': 'Compañias contables',
    'summary': 'Copia documentos de una compañia de gestion a otras compañias contables',
    'version': '1.0.1',
    'author': 'Chroma',
    'website': 'https://www.chroma.agency',
    "category": "Accounting",
    "depends": ['base','account','sale','sale_purchase','purchase','stock'],
    'data': [
        'views/purchase.order.xml',
        'views/sale.order.xml',
    ],
    'installable': True,
    'license': 'GPL-3',
}
