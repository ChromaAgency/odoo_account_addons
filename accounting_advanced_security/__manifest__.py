{
    'name': 'Seguridad por grupos',
    'summary': 'Limita la accesibilidad de los roles del usuario mediante grupos',
    'version': '17.0.9.0',
    'author': 'Chroma',
    'website': 'https://portal.chroma.agency/',
    "category": "Security",
    "depends": ['base','account','purchase'],
    'data': [
        'views/res.partner.xml',
        'views/account.journal.xml',
        'security/ir.rule.xml',
 
    ],
    'installable': True,
    'license': 'GPL-3',
}
