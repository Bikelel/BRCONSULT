# -*- coding: utf-8 -*-

from odoo import api, fields, models


class PrestationScaffoldingOperatingLoad(models.Model):
    _name = "prestation.scaffolding.operating.load"
    _description = "Prestation scaffolding operating load"

    name = fields.Char("Name")
    prestation_id = fields.Many2one('prestation.prestation', 'Prestation')
    scaffolding_class_id = fields.Many2one('prestation.scaffolding.class', string="Classe de l'échafaudage")
    operating_overload = fields.Integer("Surcharge d'exploitation")
    precision = fields.Html("Précision")
    
    @api.onchange('scaffolding_class_id')
    def onchange_scaffolding_class_id(self):
        if self.scaffolding_class_id:
            self.operating_overload = self.scaffolding_class_id.operating_overload
