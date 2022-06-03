# -*- coding: utf-8 -*-
from odoo import api, fields, models


class Partner(models.Model):
    _inherit = "res.partner"
    
    region_id = fields.Many2one('res.partner.region', 'Région', compute='_compute_departement_region', store=True)
    departement_id = fields.Many2one('res.partner.departement', 'Département', compute='_compute_departement_region', store=True)
    
    @api.depends('zip')
    def _compute_departement_region(self):
        for partner in self:
            
            if partner.zip:
                # reccherche de departement de 3 caractère
                departement = self.env['res.partner.departement'].sudo().search([('code', '=', partner.zip[:3])], limit=1)
                # reccherche de departement de 2 caractère
                if not departement:
                    departement = self.env['res.partner.departement'].sudo().search([('code', '=', partner.zip[:2])], limit=1)

                if departement:
                    partner.sudo().write({'departement_id': departement.id,
                                          'region_id': departement.region_id.id,})
                else:
                    partner.sudo().write({'departement_id': False,
                                          'region_id': False
                                         })
            else:
                partner.sudo().write({'departement_id': False,
                                          'region_id': False
                                         })
                    
                
    
