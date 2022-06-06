# -*- coding: utf-8 -*-
{
    'name': "Br consult sync calendar",

    'summary': """
        Synchronisation de la prestation avec calendrier
        """,

    'description': """
        Synchronisation de la prestation avec calendrier
    """,

    'author': "Hedi Adouni",
#     'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',
    'license': 'LGPL-3',
    # any module necessary for this one to work correctly
    'depends': ['base', 'br_consult', 'calendar'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        #'views/views.xml',
        #'views/templates.xml',
    ],

}
