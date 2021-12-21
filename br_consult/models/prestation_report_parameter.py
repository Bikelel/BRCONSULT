# -*- coding: utf-8 -*-

from odoo import api, fields, models


class PrestationReportParameter(models.Model):
    _name = "prestation.report.parameter"
    _description = "Prestation Report parameter"

    name = fields.Char("Name")
    installation_compliance = fields.Html("Conformité de l'installation")
    scope_mission = fields.Html("Périmètre de la mission")
    adequation_exam = fields.Html("Examen d'adéquation")
    