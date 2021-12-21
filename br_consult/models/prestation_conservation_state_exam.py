# -*- coding: utf-8 -*-
from odoo import api, fields, models


class PrestationConservationStateExam(models.Model):
    _name = "prestation.conservation.state.exam"
    _description = "Prestation conservation state exam"

    name = fields.Char("Nom")
    conservation_state_id = fields.Many2one("prestation.conservation.state", string ="Etat de conservation") 
    inspection_type = fields.Selection(related="conservation_state_id.inspection_type")
    installation_type = fields.Selection(related="conservation_state_id.inspection_type")
    prestation_id = fields.Many2one("prestation.prestation", string="Prestation")
    opinion = fields.Selection([('yes', 'Satisfait'), 
                                ('no', 'Non satisfait'),
                                ('wo', 'Sans Objet')], string="Avis")

