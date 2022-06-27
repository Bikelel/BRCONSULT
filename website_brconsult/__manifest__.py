# -*- coding: utf-8 -*-
{
    'name': "Website brconsult",

    'summary': """
        Portail Br consult
        """,

    'description': """
        Portail Br consult
    """,

    'author': "Hedi Adouni",
    #'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Portal',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'portal', 'br_consult'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/prestation_templates.xml',
        'data/mail_template_data.xml',
    ],
    
    'assets': {
        'web.assets_backend': [
            
            'website_brconsult/static/src/js/date_portal.js',
        ],
        'web.assets_frontend': [
            
            'website_brconsult/static/src/js/date_portal.js',
        ],
        'web._assets_common_scripts': [
            'web/static/lib/moment/locale/fr.js',
            'website_brconsult/static/src/js/date_portal.js',
        ],
    },

}
