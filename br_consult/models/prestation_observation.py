# -*- coding: utf-8 -*-

from odoo import api, fields, models


class PrestationObservation(models.Model):
    _name = "prestation.observation"
    _description = "Prestation Observation"

    name = fields.Char("Name", required=True)
    type = fields.Selection([
        ('adequacy_exam', "Examen d'adéquation"),
        ('assembly_exam', "Examen de montage et d'installation"),
        ('conservation_state_exam', "Examen de l'état de conservation")], string="Type", required=True)
   