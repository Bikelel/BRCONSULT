# -*- coding: utf-8 -*-

{
    'name': 'French address',
    'version': '1.0',
    'category': 'Tools',

    'summary': """
        Add Department and region to address""",
    'author': "Hedi Adouni",


    'depends': [
        'base',
        'contacts',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/region_views.xml',
        'views/partner_view.xml'
    ],
    'application': True,
}
