# -*- coding: utf-8 -*-

from odoo import api, fields, models


class PrestationReportParameter(models.Model):
    _name = "prestation.report.parameter"
    _description = "Prestation Report parameter"

    name = fields.Char("Name")
    inspection_type = fields.Selection([
        ('echafaudage', 'Echafaudage'),
        ('levage', 'Levage'),
    ], copy=False, string="Type d'inspection")
    installation_type = fields.Selection([
        ('PSE', 'Plateforme suspendue électrique'),
        ('PSM', 'Plateforme suspendue manuelle'),
        ('PWM', 'Plateforme de travail sur mat'),
        ('ASC', "Ascenseur de chantier"),
        ('PTR', 'Plateforme de transport'),
        ('MMA', 'Monte-matériaux'),
        ('TRE', 'Treuil'),
        ('PAE', 'Palan motorisé'),
        ('PAM', 'Palan manuel'),
    ], copy=False, string="Type d'installation")
    installation_compliance = fields.Html("Conformité de l'installation")
    scope_mission = fields.Html("Périmètre de la mission")
    adequation_exam = fields.Html("Examen d'adéquation")
    assembly_exam = fields.Html("Examen de montage")
    conservation_state = fields.Html("Examen de l'etat de conservation")
    good_functionning = fields.Html("Examen de bon fonctionnement")
    epreuve_statique = fields.Html("Epreuves statiques")
    epreuve_dynamique = fields.Html("Epreuves dynamiques")
