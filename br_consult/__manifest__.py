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
    'depends': ['base', 'portal', 'contacts', 'report_qweb_element_page_visibility', 'project', 'mail', 'l10n_fr_department'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'data/ir_sequence_data.xml',
        'views/menu_item_views.xml',
        'views/prestation_stage_views.xml',
        'views/prestation_constat_views.xml',
        'views/br_prestation_views.xml',
        'views/prestation_message_label_views.xml',
        'views/prestation_scaffolding_class_views.xml',
        'data/prestation_stage_data.xml',
        'data/prestation_scaffolding_class.xml',
        'views/prestation_image_views.xml',
        'views/res_partner_views.xml',
        'views/res_company_views.xml',
        'views/res_users_views.xml',
        'views/prestation_observation_views.xml',
        'views/prestation_verification_point_views.xml',
        'data/prestation_motif_rs.xml',
        'views/prestation_motif_rs_views.xml',
        'data/prestation_other_device.xml',
        'views/prestation_other_device_views.xml',
        'data/prestation_soil_support_data.xml',
        'views/prestation_soil_support_data_views.xml',
        'views/prestation_anchor_type_views.xml',
        'data/prestation_anchor_type.xml',
        'data/prestation_work_nature.xml',
        'views/prestation_work_nature_views.xml',
        'views/prestation_mark_views.xml',
        'data/prestation_mark.xml',
        'data/prestation_localisation.xml',
        'views/prestation_localisation_views.xml',
        'data/prestation_characteristic.xml',
        'views/prestation_characteristic_views.xml',
        'report/prestation_report_template.xml',
        'report/external_layout_brconsult.xml',
        'views/prestation_anchor_support_data_views.xml',
        'data/prestation_anchor_support_data.xml',
        'views/prestation_report_parameter_views.xml',
        'data/prestation_levage_installation_use.xml',
        'views/prestation_levage_installation_use.xml',
        'views/prestation_conservation_state_views.xml',
        'views/prestation_good_functioning_views.xml',
        'views/prestation_levage_characteristic_suspended_platform_views.xml',
        ##### caractéristique levege ####
        'data/characteristic/prestation_suspended_platform_location.xml',
        'views/characteristic/prestation_suspended_platform_location_views.xml',
        'data/characteristic/prestation_suspended_platform_access.xml',
        'views/characteristic/prestation_suspended_platform_access_views.xml',
        'data/characteristic/prestation_suspended_platform_constitution.xml',
        'views/characteristic/prestation_suspended_platform_constitution_views.xml',
        'data/characteristic/prestation_suspended_platform_mark.xml',
        'views/characteristic/prestation_suspended_platform_mark_views.xml',
        'data/characteristic/prestation_suspended_platform_assembly.xml',
        'views/characteristic/prestation_suspended_platform_assembly_views.xml',
        'data/characteristic/prestation_suspended_platform_mark_treuil.xml',
        'views/characteristic/prestation_suspended_platform_mark_treuil_views.xml',
        'data/characteristic/prestation_suspended_platform_cable_diameter.xml',
        'views/characteristic/prestation_suspended_platform_cable_diameter_views.xml',
        'data/characteristic/prestation_suspended_platform_suspension.xml',
        'views/characteristic/prestation_suspended_platform_suspension_views.xml',
        'data/characteristic/prestation_suspended_platform_suspension_location.xml',
        'views/characteristic/prestation_suspended_platform_suspension_location_views.xml',
        'data/characteristic/prestation_suspended_platform_suspension_mark.xml',
        'views/characteristic/prestation_suspended_platform_suspension_mark_views.xml',
        'data/characteristic/prestation_suspended_platform_cmu.xml',
        'views/characteristic/prestation_suspended_platform_cmu_views.xml',
        'data/characteristic/prestation_platform_mark.xml',
        'views/characteristic/prestation_platform_mark_views.xml',
        'views/prestation_levage_characteristic_platform_views.xml',
        'data/characteristic/prestation_platform_assembly_mat.xml',
        'views/characteristic/prestation_platform_assembly_mat_views.xml',
        'data/characteristic/prestation_platform_section_mat.xml',
        'views/characteristic/prestation_platform_section_mat_views.xml',
        'data/characteristic/prestation_platform_fixation_mat.xml',
        'views/characteristic/prestation_platform_fixation_mat_views.xml',
        'data/characteristic/prestation_platform_speed_unit.xml',
        'views/characteristic/prestation_platform_speed_unit_views.xml',
        'data/characteristic/prestation_platform_wind_speed_max.xml',
        'views/characteristic/prestation_platform_wind_speed_max_views.xml',
        'views/prestation_levage_characteristic_palan_views.xml',
        'data/characteristic/prestation_platform_mark_palan.xml',
        'views/characteristic/prestation_platform_mark_palan_views.xml',
        'data/mail_template_data.xml',
        'data/ir_cron_data.xml',
        
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
