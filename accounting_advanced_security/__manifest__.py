{
    'name': 'Seguridad por grupos',
    'summary': 'Limita la accesibilidad de los roles del usuario mediante grupos',
    'version': '0.9',
    'author': 'Making Argentina',
    'website': 'https://www.making.com.ar',
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
