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
    'depends': ['base', 'portal'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'data/ir_sequence_data.xml',
        'views/menu_item_views.xml',
        'views/prestation_stage_views.xml',
        'views/br_prestation_views.xml',
        'views/prestation_message_label_views.xml',
        'views/prestation_scaffolding_class_views.xml',
        'data/prestation_stage_data.xml',
        'data/prestation_scaffolding_class.xml',
        'views/prestation_image_views.xml',
    ],
    'installable': True,
    'auto_install': False,
    'license': 'LGPL-3',
    "assets": {
        "web.assets_backend": [
            "br_consult/static/src/css/backend.less"
        ]
    }
}
