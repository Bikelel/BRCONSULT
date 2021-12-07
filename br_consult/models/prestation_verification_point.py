# -*- coding: utf-8 -*-

from odoo import api, fields, models


class PrestationVerificationPoint(models.Model):
    _name = "prestation.verification.point"
    _description = "Prestation Verification Point"

    name = fields.Char("Name")
    type = fields.Selection([
        ('adequacy_exam', "Examen d'adéquation"),
        ('assembly_exam', "Examen de montage et d'installation"),
        ('conservation_state_exam', "Examen de l'état de conservation")], string="Type")
    observation_ids = fields.Many2many('prestation.observation', string="Observations")
    observations = fields.Text("Observations txt")
   