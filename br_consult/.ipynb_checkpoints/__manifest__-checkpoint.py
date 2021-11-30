# -*- coding: utf-8 -*-
{
    'name': "BR Consult",

    'summary': """
        Nouveau module pour BR Consult
        
        """,


    'author': "BR Consult",
    'website': "http://www.brconsult.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Project',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'data/ir_sequence_data.xml',
        'views/br_prestation_view.xml',
#         'views/templates.xml',
    ],
    'installable': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
