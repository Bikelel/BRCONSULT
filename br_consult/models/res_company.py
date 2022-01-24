# -*- coding: utf-8 -*-
import base64

from odoo import api, fields, models, tools, _

class Company(models.Model):
    _inherit = "res.company"

    prestation_duration = fields.Float("Durée d'une prestation (en heure)", default=2)
