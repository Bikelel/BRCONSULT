# -*- coding: utf-8 -*-

from odoo import models, fields, api, _, SUPERUSER_ID, tools


class Prestation(models.Model):
    _name = 'prestation.prestation'
    _description = 'Prestation'
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin']
    
    def default_stage(self):
        phase1 = self.env['prestation.stage'].search([('state', '=', 'phase1')], limit=1)
        return phase1.id

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
    requested_date = fields.Date('Date de la demande')
    verification_date = fields.Datetime('Date de vérification', default=fields.Datetime.now)
    partner_contact = fields.Char("Représentée par")
    user_id = fields.Many2one('res.users', 'Vérificateur', default=lambda self: self.env.user)
    stage_id = fields.Many2one(
        'prestation.stage', string='Etape', index=True, tracking=True, readonly=False, store=True,
        copy=False, group_expand='_read_group_stage_ids', ondelete='restrict', default=default_stage)
    state = fields.Selection(string='Status', readonly=True, copy=False, index=True, related='stage_id.state')
    title_label = fields.Text("Titre de prestation", store = True)
    message_label = fields.Text("Code de l'article", store = True)
    site_address = fields.Text("Adresse de chantier")
    site_localisation = fields.Char("Localisation")
    prensent_contact = fields.Char("Nom de la personne présente")
    scaffolding_surface = fields.Float("Surface d'échafaudage annoncée (m2)")
    inspected_scaffolding_surface = fields.Float("Surface d'échafaudage inspectée (m2)")
    favorable_opinion = fields.Boolean('Avis favorable')
    opinion_with_observation = fields.Boolean('Avec observation')
    defavorable_opinion = fields.Boolean('Avis defavorable')
    comment_observation_fiche = fields.Html("Commentaires Observation")
    visa_user_id = fields.Binary('Visa inspecteur', related='user_id.visa_user_id')
    contrat_ref = fields.Char('Contrat réf')
    scope_mission_date = fields.Date('Date Périmètre de la mission')
    comment_scope_mission = fields.Html("Commentaires Périmètre de la mission")
    scaffolding_mark_ids = fields.One2many('prestation.scaffolding.mark', 'prestation_id', 'Marques')
    scaffolding_characteristic_ids = fields.One2many('prestation.scaffolding.characteristic', 'prestation_id', 'Caractéristiques')
    comment_scaffolding_characteristic = fields.Html("Commentaires Caractéristique de l'échafaudage")
    adequacy_exam_ids = fields.One2many('prestation.adequacy.exam', 'prestation_id', "Examen d'adéquation")
    is_pare_gravats = fields.Selection([('yes', 'Oui'), ('no', 'Non')], string="Présence d'un pare-gravats")
    is_other_device = fields.Selection([('yes', 'Oui'), ('no', 'Non')], string="Présence d'un autre dispositif")
    other_device = fields.Selection([
        ('net', 'Filet'), 
        ('reinforced_polyane', 'Polyane armé'),
        ('cladding', 'Bardage'),
        ('advertising_tarpaulin', 'Bâche publicitaire'),
        ('other', 'Autre')], string="Autre dispositif")
    other_device_char = fields.Char("Autre dispositif à compléter")
    scaffolding_operating_load_ids = fields.One2many('prestation.scaffolding.operating.load', 'prestation_id', "Charge d'exploitation de l'échafaudage par défaut")
    security_register = fields.Selection([('yes', 'Oui'), ('no', 'Non')], string="Registre de sécurité")
    manufacturer_instructions = fields.Boolean("Notice constructeur")
    execution_plan = fields.Boolean("Plan d'exécution (PE)")
    calculation_notice = fields.Boolean("Notice de calcul (NDC)")
    maintenance_log = fields.Boolean("Carnet de maintenance")
    soil_support_data = fields.Selection([
        ('concrete', 'Béton'), 
        ('bitume', 'Bitume'),
        ('topsoil', 'Terre végétale'),
        ('roof', 'Toiture'),
        ('wall_cap', 'Murette et casquette'),
        ('other', 'Autre')], string="Données relatives au sol ou de support d'implantation")
    other_soil_support_data = fields.Char("Autre données relatives au sol ou de support d'implantation")
    anchor_type = fields.Selection([
        ('ankles_ring', 'Chevilles + anneau'), 
        ('struts', 'Etrésillons'),
        ('cravatage', 'Cravatage'),
        ('other_stable', 'Autre stable'),
        ('other', 'Autre')], string="Type d'ancrage")
    other_anchor_type = fields.Char("Autre Type d'ancrage")
    ankles_type = fields.Selection([
        ('nylon_ankles', 'Chevilles en nylon'), 
        ('expansion_ankles', 'Chevilles à expansion'), 
        ('chemical_ankles', 'Chevilles chimique'), 
        ('screw_eyebolt', 'Pitons à visser')], string="Type de chevilles")
    anchor_data_number = fields.Float("Nombre constaté (données d'ancrage)")
    anchor_data_theoretical_number = fields.Float("Nombre théorique requis (données d'ancrage)", compute='compute_anchor_data_number', store=True)
    anchor_data_difference_number = fields.Float("Nombre de différence (données d'ancrage)", compute='compute_anchor_data_number', store=True)


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
    
    @api.onchange('inspection_type', 'installation_type', 'verification_type')
    def onchange_label_header(self):
        label = False
        if self.inspection_type == 'echafaudage':
            label = self.env['prestation.message.label'].search([('inspection_type', '=', self.inspection_type)], limit=1)
        elif self.inspection_type == 'levage':
            if self.installation_type:
                label = self.env['prestation.message.label'].search([('inspection_type', '=', self.inspection_type), ('installation_type', '=', self.installation_type)])
        if label:
            self.title_label = label.name
            self.message_label = label.description
        else:
            self.title_label = ''
            self.message_label = ''
            
    @api.onchange('is_other_device')
    def onchange_is_other_device(self):
        if self.is_other_device == 'no':
            self.other_device = None
            self.other_device_char = ''
    
    @api.depends('anchor_data_number', 'is_other_device')
    def compute_anchor_data_number(self):
        for rec in self:
            if rec.anchor_data_number:
                if rec.is_other_device == 'yes':
                    anchor_data_theoretical_number = rec.anchor_data_number / 12
                elif rec.is_other_device == 'no':
                    anchor_data_theoretical_number = rec.anchor_data_number / 24
                else:
                    anchor_data_theoretical_number = 0.0
                
                rec.anchor_data_theoretical_number = anchor_data_theoretical_number
                rec.anchor_data_difference_number = rec.anchor_data_number - anchor_data_theoretical_number

