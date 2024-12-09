# -*- coding: utf-8 -*-
{
    'name': 'Compañias contables',
    'summary': 'Copia documentos de una compañia de gestion a otras compañias contables',
    'version': '18.0.1.0',
    'author': 'Chroma',
    'website': 'https://www.chroma.agency',
    "category": "Accounting",
    "depends": ['base','account','sale','sale_purchase','purchase','stock'],
    'data': [
        'views/purchase.order.xml',
        'views/sale.order.xml',
        'views/stock.picking.type.xml',
    ],
    'installable': True,
    'license': 'GPL-3',
}
