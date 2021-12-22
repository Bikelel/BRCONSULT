# -*- coding: utf-8 -*-

from odoo import api, fields, models


class PrestationLevageCharacteristicPlatform(models.Model):
    _name = "prestation.levage.characteristic.platform"
    _description = "Prestation levage characteristic platform"

    name = fields.Char("N° de la plateforme suspendue")
    prestation_id = fields.Many2one('prestation.prestation', 'Prestation')
    installation_type = fields.Selection(related="prestation_id.installation_type")
    platform_location_id = fields.Many2one('prestation.suspended.platform.location', "Localisation de la plateforme")
    platform_access_id = fields.Many2one('prestation.suspended.platform.access', "Acces à la plateforme")
    length_platform = fields.Float("Longeur de la plateforme")
    width_platform = fields.Float("Largeur de la plateforme")
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
    num_fabrication = fields.Char("Numéro(s) de fabrication")
    alimentation = fields.Selection([
        ('triphase', 'Triphase'),
        ('monophase', 'Monophase'),
    ], string="Alimentation")
    platform_assembly_id = fields.Many2one('prestation.suspended.platform.assembly', "Assemblage des modules")
    platform_assembly_mat_id = fields.Many2one('prestation.platform.assembly.mat', "Assemblage des élément MAT(s)")
    suspension_type = fields.Selection([
        ('monomat', 'Monomât'),
        ('bimats', 'bimâts'),
    ], string="Type de suspension")
    nb_mat = fields.Integer("Nombre des éléments de MAT")
    dimension_mat = fields.Float("Dimension des éléments de MAT", default=1.5)
    hauteur_elevation = fields.Float(string="HAUTEUR ELEVATION", compute='_compute_hauteur_elevation', store=True)
    
    constructeur_cmu = fields.Char("CMU Constructeur")
    autorized_cmu = fields.Char("CMU autorisée")
    comment_cmu = fields.Html("Commentaire CMU")
    
    @api.depends('nb_mat','dimension_mat')
    def _compute_hauteur_elevation(self):
        for record in self:
            if record.nb_mat and record.dimension_mat:
                record.hauteur_elevation = record.dimension_mat * record.nb_mat
    