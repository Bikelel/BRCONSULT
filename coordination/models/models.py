# -*- coding: utf-8 -*-

from odoo import models, fields, api


class coordination(models.Model):
    _name = 'coordination.coordination'
    _description = 'coordination.coordination'

    name = fields.Char()
    value = fields.Integer()
    
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()

#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100

    user_id = fields.Many2one('res.users', 'Coordonateur', tracking=True, required=True)
#    email_partner_ids = fields.Many2many('res.partner', string="Emails")
    partner_id = fields.Many2one('res.partner', "Adresse e-mail de l'interlocuteur", tracking=True, required=True)
    address_site = fields.Text("Adresse du chantier")
    works_type = fields.Char("Type de travaux")
    kanban_color = fields.Char("Kanban")
#    name = fields.Char("N° dossier", default=lambda self: _('New'), copy=False)
                                 
