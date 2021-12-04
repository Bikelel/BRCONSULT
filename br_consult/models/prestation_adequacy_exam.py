# -*- coding: utf-8 -*-

from odoo import api, fields, models


class PrestationAdequacyExam(models.Model):
    _name = "prestation.adequacy.exam"
    _description = "Prestation Adequacy Exam"

    name = fields.Char("Name")
    prestation_id = fields.Many2one('prestation.prestation', 'Prestation')
    works_nature = fields.Selection([
        ('facelift', 'Ravalement de façade'),
        ('facade_zinc', 'Zinguerie en façade'),
        ('roof_covering', 'Couverture en toiture'),
        ('cladding', 'Bardage'),
        ('thermal_insulation', 'Isolation thermique'),
        ('other', 'Autre')], string="Nature des travaux")
    
    other_nature = fields.Char("Autre nature")
    precision = fields.Char("Précision")
    is_examined = fields.Selection([
        ('yes', 'Oui'),
        ('no', 'Non')], string="Examiné")
    