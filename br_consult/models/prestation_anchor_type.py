# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError

class PrestationAnchorType(models.Model):
    _name = "prestation.anchor.type"
    _description = "Prestation anchor type"

    name = fields.Char("Name")
    sequence = fields.Integer('Séquence', default=10)
    
    @api.ondelete(at_uninstall=False)
    def _unlink_except_confirmed(self):
        if self.id == 1:
            raise UserError(_('You can not remove this type.'))
