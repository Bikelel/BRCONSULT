# -*- coding: utf-8 -*-

from odoo import api, fields, models


class PrestationLevageCharacteristicPlatform(models.Model):
    _name = "prestation.levage.characteristic.palan"
    _description = "Prestation levage characteristic palan"

    name = fields.Char("Numéro")
    prestation_id = fields.Many2one('prestation.prestation', 'Prestation')
    installation_type = fields.Selection(related="prestation_id.installation_type")
    palan_location_id = fields.Many2one('prestation.suspended.platform.location', "Localisation")
    palan_access_id = fields.Many2one('prestation.suspended.platform.access', "Acces")
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
    other_suspension_mode = fields.Char("Autre")
    cote_poutre = fields.Char("Côtes de la poutre")
    noted_lest = fields.Char("Lest constaté (kg)")
    preconized_lest = fields.Char("Lest préconisé (kg) ")
    height = fields.Float("Hauteur d'élévation (en mètre)")
    palan_mark_id = fields.Many2one('prestation.platform.mark', "Marque")
    modele = fields.Char("Modèle")
    num_fabrication = fields.Char("Numéro(s) de fabrication")
    circulation_year = fields.Char("Année de mise en circulation")
    capacity_nominale = fields.Char("Capacité nominale")
    capacity_taree = fields.Char("Capacité tarée")
    alimentation = fields.Selection([
        ('triphase', 'Triphase'),
        ('monophase', 'Monophase'),
    ], string="Alimentation")
    move_speed = fields.Float("Vitesse de déplacement vertical (m/min)")
    wind_speed_max_id = fields.Many2one('prestation.platform.wind.speed.max', string="Vitesse maximale de vent autorisée")
    number_brins_builder = fields.Char("Nombre de brins x Diamètre de la chaîne constructeur (en millimètre)")
    number_brins_noted = fields.Char("Nombre de brins x Diamètre de la chaîne constaté (en millimètre):")
    