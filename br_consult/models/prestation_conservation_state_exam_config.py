# -*- coding: utf-8 -*-
from odoo import api, fields, models


class PrestationConservationStateExamConfig(models.Model):
    _name = "prestation.conservation.state.exam.config"
    _description = "Prestation conservation state exam config"

    name = fields.Char("Nom", required=True)

