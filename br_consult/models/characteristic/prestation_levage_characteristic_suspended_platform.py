# -*- coding: utf-8 -*-

from odoo import api, fields, models


class PrestationLevageCharacteristicSuspendedPlatform(models.Model):
    _name = "prestation.levage.characteristic.suspended.platform"
    _description = "Prestation levage characteristic suspended platform"

    name = fields.Char("N° de la plateforme suspendue")
    prestation_id = fields.Many2one('prestation.prestation', 'Prestation')
    height_platform = fields.Float("Hauteur plateforme")
    length_platform = fields.Float("Largeur plateforme")
    suspended_platform_location_id = fields.Many2one('prestation.suspended.platform.location', "Localisationde la plateforme suspendue")
    suspended_platform_access_id = fields.Many2one('prestation.suspended.platform.access', "Acces plateforme suspendue")
    suspended_platform_constitution_id = fields.Many2one('prestation.suspended.platform.constitution', "Constitution plateforme suspendue")
    suspended_platform_mark_id = fields.Many2one('prestation.suspended.platform.mark', "Marque plateforme suspendue")
    suspended_platform_assembly_id = fields.Many2one('prestation.suspended.platform.assembly', "Assemblage plateforme suspendue")
    suspended_platform_mark_treuil_id = fields.Many2one('prestation.suspended.platform.mark.treuil', "Marque treuil plateforme suspendue")
    type_treuil = fields.Char("Type de treuil")
    alimentation = fields.Selection([
        ('triphase', 'Triphase'),
        ('monophase', 'Monophase'),
    ], string="Alimentation")
    numero_treuil = fields.Char("N° treuil")
    capacity_treuil = fields.Char("Capacité treuil")
    is_taree = fields.Boolean("A une capacité tarée")
    capacity_taree = fields.Float("Capacité tarée")
    suspended_platform_cable_diameter_id = fields.Many2one('prestation.suspended.platform.cable.diameter', "Diametre des cables (en mm)")
    
    suspended_platform_suspension_id = fields.Many2one('prestation.suspended.platform.suspension', "Suspension par")
    suspended_platform_suspension_location_id = fields.Many2one('prestation.suspended.platform.suspension.location', "Localisation des suspensions")
    suspended_platform_suspension_mark_id = fields.Many2one('prestation.suspended.platform.suspension.mark', "Marque des suspensions")
    vertical_guide = fields.Selection([
        ('cable', 'Cables'),
        ('mat', 'Mat(s)'),
        ('sans_objet', 'Sans objet'),
    ], string="Guidage vertical")
