# -*- coding: utf-8 -*-

from odoo import api, fields, models


class PrestationStage(models.Model):
    _name = "prestation.stage"
    _description = "Prestation Stages"
    _rec_name = 'name'
    _order = "sequence, name, id"

    @api.model
    def default_get(self, fields):
        """ As we have lots of default_team_id in context used to filter out
        leads and opportunities, we pop this key from default of stage creation.
        Otherwise stage will be created for a given team only which is not the
        standard behavior of stages. """
        if 'default_team_id' in self.env.context:
            ctx = dict(self.env.context)
#             ctx.pop('default_team_id')
            self = self.with_context(ctx)
        return super(PrestationStage, self).default_get(fields)

    name = fields.Char("Nom de l'étape", required=True, translate=True)
    sequence = fields.Integer('Séquence', default=1)
    state = fields.Selection([
        ('phase1', 'Phase I - Création'),
        ('phase2', 'Phase II - Exploitation'),
        ('phase3', 'Phase III - Validation'),
        ('phase4', 'Phase IV - Envoi'),
        ], string='Status', readonly=True, copy=False, index=True)
