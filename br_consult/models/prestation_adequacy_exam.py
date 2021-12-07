# -*- coding: utf-8 -*-

from odoo import api, fields, models


class PrestationAdequacyExam(models.Model):
    _name = "prestation.adequacy.exam"
    _description = "Prestation Adequacy Exam"

    name = fields.Char("Name")
    prestation_id = fields.Many2one('prestation.prestation', 'Prestation')
    works_nature_id = fields.Many2one('prestation.work.nature', string="Nature des travaux")
    precision = fields.Char("Précision")
    is_examined = fields.Selection([
        ('yes', 'Oui'),
        ('no', 'Non')], string="Examiné")
    