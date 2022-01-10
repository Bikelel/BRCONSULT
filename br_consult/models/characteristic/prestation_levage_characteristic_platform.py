# -*- coding: utf-8 -*-

from odoo import api, fields, models


class PrestationLevageCharacteristicPlatform(models.Model):
    _name = "prestation.levage.characteristic.platform"
    _description = "Prestation levage characteristic platform"

    name = fields.Char("Numéro")
    prestation_id = fields.Many2one('prestation.prestation', 'Prestation')
    installation_type = fields.Selection(related="prestation_id.installation_type")
    platform_location_id = fields.Many2one('prestation.suspended.platform.location', "Localisation de la plateforme")
    platform_access_id = fields.Many2one('prestation.suspended.platform.access', "Acces à la plateforme")
    length_platform = fields.Float("Longeur de la plateforme")
    width_platform = fields.Float("Largeur de la plateforme")
    hauteur_platform = fields.Float("Hauteur")
    presence_extention = fields.Selection([
        ('yes', 'Oui'),
        ('no', 'Non'),
    ], string="Présence d'extension")
    width_extention = fields.Float("Largeur de l'extension")
    maximum_range = fields.Float("Portée maximale(m)")
    maximum_offset = fields.Float("Déport maximale(m)")
    platform_constitution_id = fields.Many2one('prestation.suspended.platform.constitution', "Constitution")
    
    platform_mark_id = fields.Many2one('prestation.platform.mark', "Marque de la plateforme")
    platform_type = fields.Char("Type de la plateforme")
    modele = fields.Char("Modèle")
    num_fabrication = fields.Char("Numéro(s) de fabrication")
    fabrication_year = fields.Char("Année de fabrication")
    circulation_year = fields.Char("Année de mise en circulation")
    level_service = fields.Char("Desserte des niveaux")
    alimentation = fields.Selection([
        ('triphase', 'Triphase'),
        ('monophase', 'Monophase'),
    ], string="Alimentation")
    
    open_close_doors = fields.Selection([
        ('verticale', 'Verticale'),
        ('horizontale', 'Horizontale'),
        ('other', 'Autre'),
    ], string="Ouverture/fermeture des portes")
    other_open_close_doors = fields.Char("Autre")
    presence_roof = fields.Selection([
        ('yes', 'Oui'),
        ('no', 'Non'),
    ], string="Présence d'un toit")
    
    platform_assembly_id = fields.Many2one('prestation.suspended.platform.assembly', "Assemblage des modules")
    platform_assembly_mat_id = fields.Many2one('prestation.platform.assembly.mat', "Assemblage des élément MAT(s)")
    suspension_type = fields.Selection([
        ('monomat', 'Monomât'),
        ('bimats', 'bimâts'),
    ], string="Type de suspension")
    platform_section_mat_id = fields.Many2one('prestation.platform.section.mat', "Section des élément MAT(s)")
    nb_mat = fields.Integer("Nombre des éléments de MAT")
    dimension_mat = fields.Float("Dimension des éléments de MAT", default=1.5)
    hauteur_elevation = fields.Float(string="Hauteur d'élévation (mètre)", compute='_compute_hauteur_elevation', store=True)
    platform_fixation_mat_id = fields.Many2one('prestation.platform.fixation.mat', "Mode de fixation des élément de MAT(s)")
    fixation_position = fields.Char("Positionnement des Fixations")
    move_speed = fields.Float("Vitesse de déplacement vertical")
    speed_unit_id = fields.Many2one('prestation.platform.speed.unit', "Unité de vitesse verticale")
    wind_speed_max_id = fields.Many2one('prestation.platform.wind.speed.max', string="Vitesse maximale de vent autorisée")
    constructeur_cmu = fields.Char("CMU Constructeur")
    autorized_cmu = fields.Char("CMU autorisée")
    comment_cmu = fields.Html("Commentaire CMU")
    
    @api.depends('nb_mat','dimension_mat')
    def _compute_hauteur_elevation(self):
        for record in self:
            if record.nb_mat and record.dimension_mat:
                record.hauteur_elevation = record.dimension_mat * record.nb_mat
    