# -*- coding: utf-8 -*-

from odoo import models, fields, api, _, SUPERUSER_ID


class Prestation(models.Model):
    _name = 'br.prestation'
    _description = 'br.prestation'

    name = fields.Char("N° Rapport", default=lambda self: 'New')
    partner_id = fields.Many2one('res.partner', string="Entreprise")
    inspection_type = fields.Selection([
        ('echafaudage', 'Echafaudage'),
        ('levage', 'Levage'),
    ], copy=False, string="Type d'inspection")
    installation_type = fields.Selection([
        ('PSE', 'Plateforme suspendue électrique'),
        ('PSM', 'Plateforme suspendue manuelle'),
        ('PWM', 'Plateforme de travail sur mat'),
        ('ASC', "Ascenseur de chantier"),
        ('PTR', 'Plateforme de transport'),
        ('MMA', 'Monte-matériaux'),
        ('TRE', 'Treuil'),
        ('PAE', 'Palant motorisé'),
        ('PAM', 'Palant manuel'),
    ], copy=False, string="Type d'installation")
    verification_type = fields.Selection([
        ('MS', 'Mise en service'),
        ('RS', 'Remise en service'),
        ('VP', 'Vérification périodique'),
    ], copy=False, string="Type de vérification")
    date = fields.Date('Date', default=fields.Date.today())
    verification_date = fields.Datetime('Date de vérification', default=fields.Datetime.now)
    partner_contact = fields.Char("Représentée par")
    user_id = fields.Many2one('res.users', 'Vérificateur', default=lambda self: self.env.user)
    stage_id = fields.Many2one(
        'prestation.stage', string='Etape', index=True, tracking=True, readonly=False, store=True,
        copy=False, group_expand='_read_group_stage_ids', ondelete='restrict')
    state = fields.Selection([
        ('phase1', 'Phase I - Création'),
        ('phase2', 'Phase II - Validation'),
        ('phase3', 'Phase III - Exploitation'),
        ('phase4', 'Phase IV - Envoi'),
        ], string='Status', readonly=True, copy=False, index=True, default='phase1', related='stage_id.state')

    @api.model
    def create(self, vals):
        if 'company_id' in vals:
            self = self.with_company(vals['company_id'])
        if vals.get('partner_id'):
            partner = self.env['res.partner'].browse(vals.get('partner_id'))
            
            if partner.ref:
                partner_ref = partner.ref
            else:
                partner_ref = ''
            
        if vals.get('name') == 'New':
            if vals.get('inspection_type') == 'echafaudage':
                code_installation_type = 'RTU'
            elif vals.get('inspection_type') == 'levage':
                if vals.get('installation_type'):
                    code_installation_type = vals.get('installation_type')
            else:
                code_installation_type = ''
            if vals.get('verification_type'):
                code_verification_type = vals.get('verification_type')
            else:
                code_verification_type = ''
            vals['name'] = partner_ref + '-' +code_installation_type+ '-' + code_verification_type + '-' + self.env['ir.sequence'].next_by_code('sale.order') or _('New')
        
        result = super(Prestation, self).create(vals)
        return result
    
    @api.model
    def _read_group_stage_ids(self, stages, domain, order):
        stages = self.env['prestation.stage'].search([])
        search_domain = [('id', 'in', stages.ids)]
        # perform search
        stage_ids = stages._search(search_domain, order=order, access_rights_uid=SUPERUSER_ID)
        return stages.browse(stage_ids)

