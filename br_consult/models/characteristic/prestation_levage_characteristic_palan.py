# -*- coding: utf-8 -*-

from odoo import api, fields, models


class PrestationLevageCharacteristicPlatform(models.Model):
    _name = "prestation.levage.characteristic.palan"
    _description = "Prestation levage characteristic palan"

    name = fields.Char("Numéro")
    prestation_id = fields.Many2one('prestation.prestation', 'Prestation')
    installation_type = fields.Selection(related="prestation_id.installation_type")
    palan_location_id = fields.Many2one('prestation.suspended.platform.location', "Localisation")
    palan_access_id = fields.Many2one('prestation.suspended.platform.access', "Accès")
    suspension_mode = fields.Selection([('chevalet', 'Chevalet'),
                                        ('portique', 'Portique'),
                                        ('grue_levage', 'Grue de levage'),
                                        ('poutre_lestees', 'Poutre métalliques lestées'),
                                        ('poutre_spitted', 'Poutre(s) métallique(s) spittée(s)'),
                                        ('potence', 'Potence'),
                                        ('echafaudage', 'Echafaudage'),
                                        ('poutre_ipn', 'Poutre IPN'),
                                        ('other', 'Autre'),
                                       ], string="Mode de suspension")
    other_suspension_mode = fields.Char(string="Autre")
    cote_poutre = fields.Char("Côtes de la poutre")
    noted_lest = fields.Float("Lest constaté (kg)")
    preconized_lest = fields.Float("Lest préconisé (kg)")
    difference_lest = fields.Float("Différence (kg)", compute='_compute_differenceLest')
    
    height = fields.Float("Hauteur d'élévation (en mètre)")
    platform_palan_mark_id = fields.Many2one('prestation.platform.mark.palan', "Marque")
    modele = fields.Char("Modèle")
    num_fabrication = fields.Char("Numéro(s) de fabrication")
    fabrication_year = fields.Char("Année de fabrication")
    circulation_year = fields.Char("Année de mise en circulation")
    capacity_nominale = fields.Char("Capacité nominale")
    #capacity_taree = fields.Char("Capacité tarée")
    is_taree = fields.Boolean("A une capacité tarée")
    capacity_taree = fields.Float("Capacité tarée")
    alimentation = fields.Selection([
        ('triphase', 'Triphase'),
        ('monophase', 'Monophase'),
    ], string="Alimentation")
    move_speed = fields.Char("Vitesse de déplacement vertical (m/min)")
    wind_speed_max_id = fields.Many2one('prestation.platform.wind.speed.max', string="Vitesse maximale du vent autorisée en service")
    number_brins_builder = fields.Char("Nombre de brins x Diamètre de la chaîne constructeur (en millimètre)")
    number_brins_noted = fields.Char("Nombre de brins x Diamètre de la chaîne constaté (en millimètre)")
    constructeur_cmu = fields.Char("CMU Constructeur (kg)")
    autorized_cmu = fields.Char("CMU autorisée (kg)")
    
    @api.depends('noted_lest', 'preconized_lest')
    def _compute_differenceLest(self):
        for rec in self:
            rec.difference_lest = rec.noted_lest - rec.preconized_lest
    