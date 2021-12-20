# -*- coding: utf-8 -*-

from odoo import api, fields, models


class PrestationVerificationPoint(models.Model):
    _name = "prestation.verification.point"
    _description = "Prestation Verification Point"

    name = fields.Char("Name")
    type = fields.Selection([
        ('adequacy_exam', "Examen d'adéquation"),
        ('assembly_exam', "Examen de montage et d'installation"),
        ('conservation_state_exam', "Examen de l'état de conservation"),
        ('epreuve_statique', "Epreuve statique"),
        ('epreuve_dynamique', "Epreuve dynamique")], string="Type")
    observations = fields.Text("Observations old")
    observation_ids = fields.One2many("prestation.observation", 'verification_point_id', "Observations")
    
   