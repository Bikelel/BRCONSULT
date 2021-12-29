# -*- coding: utf-8 -*-

from odoo import models, fields, api, _, SUPERUSER_ID, tools


class Prestation(models.Model):
    _name = 'prestation.prestation'
    _description = 'Prestation'
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin']
    
    
    def get_default_characteristic(self):
        attributes = self.env['prestation.characteristic'].search([('is_default', '=', True)])
        lines = []
        for line in attributes:
            lines.append((0, 0, {'name': line.name,
                                 'characteristic_id': line.id,
                                 'is_length': line.is_length,
                                 'is_width': line.is_width,
                                 'is_height': line.is_height,
                                 'is_surface': line.is_surface,
                                }))
        return lines
    
    def get_default_report_parameter(self):
        report_parameter_id = self.env['prestation.report.parameter'].search([], limit=1)
        if report_parameter_id:
            return report_parameter_id.id
        else:
            return False

    name = fields.Char("N° Rapport", default=lambda self: 'New', copy=False)
    report_parameter_id = fields.Many2one('prestation.report.parameter',string="Parametre du rapport", default=get_default_report_parameter)
    company_id = fields.Many2one('res.company', 'Company', required=True, index=True, default=lambda self: self.env.company)
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
        ('PAE', 'Palan motorisé'),
        ('PAM', 'Palan manuel'),
    ], copy=False, string="Type d'installation")
    verification_type = fields.Selection([
        ('MS', 'Mise en service'),
        ('RS', 'Remise en service'),
        ('VP', 'Vérification périodique'),
    ], copy=False, string="Type de vérification")
    date = fields.Date(string="Date de saisie du rapport", default=fields.Date.today())
    requested_date = fields.Date('Date de la demande')
    verification_date = fields.Datetime('Date de vérification', default=fields.Datetime.now)
    partner_contact = fields.Char("Représentée par")
    user_id = fields.Many2one('res.users', 'Vérificateur', default=lambda self: self.env.user)
    stage_id = fields.Many2one(
        'prestation.stage', string='Etape', index=True, tracking=True, readonly=False, store=True, copy=False, group_expand='_read_group_stage_ids', ondelete='restrict')
    state = fields.Selection(string='Status', readonly=True, copy=False, index=True, related='stage_id.state', default="phase1")
    title_label = fields.Text("Titre de prestation", store = True)
    message_label = fields.Text("Code de l'article", store = True)
    site_address = fields.Text("Adresse de chantier")
    site_localisation = fields.Char("Localisation")
    prensent_contact = fields.Char("Nom de la personne présente")
    scaffolding_surface = fields.Float("Surface d'échafaudage annoncée (m2)")
    inspected_scaffolding_surface = fields.Float("Surface d'échafaudage inspectée (m2)", digits="0", compute="_compute_inspected_surface", store=True)
    favorable_opinion = fields.Boolean('Avis favorable')
    opinion_with_observation = fields.Boolean('Avec observation')
    defavorable_opinion = fields.Boolean('Avis defavorable')
    comment_observation_fiche = fields.Html("Commentaires Observation")
    visa_user = fields.Binary('Visa inspecteur', related='user_id.visa_user')
    contrat_ref = fields.Char('Contrat réf')
    motif_rs_id = fields.Many2one('prestation.motif.rs', string="Motif de remise en service")
    scope_mission_date = fields.Date(string="Date du contrat")
    comment_scope_mission = fields.Html("Commentaires Périmètre de la mission")
    scaffolding_mark_ids = fields.One2many('prestation.scaffolding.mark', 'prestation_id', 'Marques')
    scaffolding_characteristic_ids = fields.One2many('prestation.scaffolding.characteristic', 'prestation_id', string="Caracteristiques", default=get_default_characteristic)
    
    comment_scaffolding_characteristic = fields.Html("Commentaires Caractéristique de l'échafaudage")
    adequacy_exam_ids = fields.One2many('prestation.adequacy.exam', 'prestation_id', "Examen d'adéquation")
    is_pare_gravats = fields.Selection([('yes', 'Oui'), ('no', 'Non')], string="Présence d'un pare-gravats")
    is_other_device = fields.Selection([('yes', 'Oui'), ('no', 'Non')], string="Présence d'un autre dispositif")
    other_device_id = fields.Many2one('prestation.other.device', string='Autre dispositif')
    scaffolding_operating_load_ids = fields.One2many('prestation.scaffolding.operating.load', 'prestation_id', "Charge d'exploitation de l'échafaudage par défaut")
    security_register = fields.Selection([('yes', 'Oui'), ('no', 'Non')], string="Registre de sécurité")
    assembly_file = fields.Selection([('yes', 'Oui'), ('no', 'Non')], string="Mise à disposition du dossier de montage")
    manufacturer_instructions = fields.Selection([('yes', 'Oui'), ('no', 'Non')], string="Mise à disposition du notice constructeur")
    execution_plan = fields.Boolean("Plan d'exécution (PE)")
    calculation_notice = fields.Boolean("Notice de calcul (NDC)")
    maintenance_log = fields.Boolean("Carnet de maintenance")
    soil_support_data_ids = fields.Many2many('prestation.soil.support.data', string="Données relatives au sol ou de support d'implantation")
    anchor_support_data_ids = fields.Many2many('prestation.anchor.support.data', string="Nature des supports d’ancrage")
    anchor_type_id = fields.Many2one('prestation.anchor.type', "Type d'ancrage")
    ankles_type = fields.Selection([
        ('nylon_ankles', 'Chevilles en nylon'), 
        ('expansion_ankles', 'Chevilles à expansion'), 
        ('chemical_ankles', 'Chevilles chimique'), 
        ('screw_eyebolt', 'Pitons à visser')], string="Type de chevilles")
    anchor_data_number = fields.Float("Nombre constaté (données d'ancrage)")
    anchor_data_theoretical_number = fields.Float("Nombre théorique requis (données d'ancrage)", compute='compute_anchor_data_number', store=True)
    anchor_data_difference_number = fields.Float("Nombre de différence (données d'ancrage)", compute='compute_anchor_data_number', store=True)
    ground_support_data = fields.Selection([
        ('transmitted', 'Transmises'), 
        ('observed_site', 'Constatées sur place')], string="Données relatives aux réactions d'appuis au sol ou au support d’accueil")
    climatic_data = fields.Selection([
        ('zone1', "Zone 1 : Vent normal 103km/  / Vent extrême 136.1 km/h - Conformément aux règles NV 65 et N 84"), 
        ('zone2', "Zone 2 : Vent normal 112km/  / Vent extrême 149.1 km/h - Conformément aux règles NV 65 et N 84"), 
        ('zone3', "Zone 3 : Vent normal 126km/  / Vent extrême 166.6 km/h - Conformément aux règles NV 65 et N 84"), 
        ('zone4', "Zone 4 : Vent normal; 138km/  / Vent extrême 182.6 km/h - Conformément aux règles NV 65 et N 84"), 
        ('zone5', "Zone 5 : Vent normal 174.6km/  / Vent extrême 230.9 km/h - Conformément aux règles NV 65 et N 84"),
    ], string="Données relatives aux charges climatiques")
    covering_nature_data = fields.Selection([
        ('transmitted', 'Transmises'), 
        ('observed_site', 'Constatées sur place')], string="Données relatives à la nature du bâchage éventuel")
    conservation_state_exam_ids = fields.One2many('prestation.conservation.state.exam', 'prestation_id', string="Examen d'état de conservation")
    good_functioning_exam_ids = fields.One2many('prestation.good.functioning.exam', 'prestation_id', string="Examen du bon fonctionnement")
    
    location_diagram = fields.Binary("Schéma de l’emplacement")
    image_ids = fields.One2many('prestation.image', 'prestation_id' ,"Photographies")
    comment_scaffolding_photographic_location = fields.Html("Commentaires localisation photographique de l'échafaudage")
    
    constat_adequacy_exam_ids = fields.One2many('prestation.constat', 'prestation_id', "Constat Examen d'adéquation", domain=[('type', '=', 'adequacy_exam')])
    constat_assembly_exam_ids = fields.One2many('prestation.constat', 'prestation_id', "Constat Examen de montage et d'installation", domain=[('type', '=', 'assembly_exam')])
    constat_conservation_state_exam_ids = fields.One2many('prestation.constat', 'prestation_id', string="Constat Examen de l'état de conservation", domain=[('type', '=', 'conservation_state_exam')])
    ############### Levage Fields ##################
    announced_installation_number = fields.Integer("Nombre d'installation annoncée(s)")
    inspected_installation_number = fields.Integer("Nombre d'installation inspectée(s)", compute="_compute_inspected_installation_number", store=True)
    protection_dispositif = fields.Selection([('yes', 'Oui'), ('no', 'Non')], string="Présence d'un dispositif de protection")
    levage_protection_dispositif = fields.Char("Dispositif de protection de levage")
    comment_protection_dispositif = fields.Html("Commentaires dispositif de protection")
    comment_assembly_exam = fields.Html("Commentaires examen de montage")
    
    constat_good_functioning_exam_ids = fields.One2many('prestation.constat', 'prestation_id', "Constat Examen de bon fonctionnement", domain=[('type', '=', 'good_functioning')])
    
    installation_use_id = fields.Many2one('prestation.levage.installation.use', "Utilisation de l'installation")
    coefficient_statique = fields.Float("Coefficient statique")
    autorised_cmu_statique = fields.Float("CMU Autorisée statique (en KG)")
    theoretical_test_load_statique = fields.Float("Charge d'épreuve théorique statique (en KG)", store="True", compute='_compute_theoretical_test_load_statique')
    reel_test_load_statique = fields.Float("Charge d'épreuve réelle statique (en KG)")
    test_duration_statique = fields.Float("Durée d’épreuve statique (en minutes)")
    elevation_height_statique = fields.Float("Hauteur d'élévation (en m)")
    comment_epreuve_statique = fields.Html("Commentaires Epreuve")
    constat_epreuve_statique_ids = fields.One2many('prestation.constat', 'prestation_id', "Constat Examen d'épreuve statique", domain=[('type', '=', 'epreuve_statique')])
    coefficient_dynamique = fields.Float("Coefficient dynamique")
    autorised_cmu_dynamique = fields.Float("CMU Autorisée dynamique (en KG)")
    theoretical_test_load_dynamique = fields.Float("Charge d'épreuve théorique dynamique (en KG)", store="True", compute='_compute_theoretical_test_load_dynamique')
    reel_test_load_dynamique = fields.Float("Charge d'épreuve réelle dynamique (en KG)")
    comment_epreuve_dynamique = fields.Html("Commentaires Epreuve dynamique")
    constat_epreuve_dynamique_ids = fields.One2many('prestation.constat', 'prestation_id', "Constat d'épreuve dynamique", domain=[('type', '=', 'epreuve_dynamique')])
    
    characteristic_suspended_platform_ids = fields.One2many('prestation.levage.characteristic.suspended.platform', 'prestation_id', "Caractéristique de la plateforme suspendue")
    
    # travail sur mat
    characteristic_platform_ids = fields.One2many('prestation.levage.characteristic.platform', 'prestation_id', "Caractéristique de la plateforme")
    
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
            vals['name'] = partner_ref + '-' +code_installation_type+ '-' + code_verification_type + '-' + self.env['ir.sequence'].next_by_code('prestation.prestation') or _('New')
            attributes_good_functioning = None
            if vals.get('inspection_type') == 'echafaudage':
                attributes_conservation_state = self.env['prestation.conservation.state'].search([('inspection_type', '=', 'echafaudage')])
            elif vals.get('inspection_type') == 'levage' and vals.get('installation_type'):
                attributes_conservation_state = self.env['prestation.conservation.state'].search([('inspection_type', '=', 'levage'), ('installation_type', '=', vals.get('installation_type'))])
                
                attributes_good_functioning = self.env['prestation.good.functioning'].search([('inspection_type', '=', 'levage'), ('installation_type', '=', vals.get('installation_type'))])
                
            else:
                attributes_conservation_state = None
                
            if attributes_conservation_state:
                lines = []
                for line in attributes_conservation_state:
                    lines.append((0, 0, {'conservation_state_id': line.id,
                                         'name': line.name}))
                
                vals.update({'conservation_state_exam_ids': lines})
            if attributes_good_functioning:
                lines = []
                for line in attributes_good_functioning:
                    lines.append((0, 0, {'good_functioning_id': line.id,
                                         'name': line.name}))
                
                vals.update({'good_functioning_exam_ids': lines})
                
                
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
            self.other_device_id = None
    
    @api.depends('scaffolding_mark_ids','scaffolding_mark_ids.inspected_surface', 'is_other_device')
    def compute_anchor_data_number(self):
        for rec in self:
            total = sum(rec.scaffolding_mark_ids.mapped('inspected_surface'))
            if total:
                if rec.is_other_device == 'yes':
                    anchor_data_theoretical_number = total / 12
                elif rec.is_other_device == 'no':
                    anchor_data_theoretical_number = total / 24
                else:
                    anchor_data_theoretical_number = 0.0
                
                rec.anchor_data_theoretical_number = anchor_data_theoretical_number
                rec.anchor_data_difference_number = rec.anchor_data_number - anchor_data_theoretical_number

    @api.onchange('assembly_file')
    def onchange_assembly_file(self):
        if self.assembly_file == 'no':
            self.execution_plan = False
            self.calculation_notice = False
            self.manufacturer_instructions = False
    
    @api.depends('coefficient_statique', 'autorised_cmu_statique')
    def _compute_theoretical_test_load_statique(self):
        for rec in self:
            if rec.autorised_cmu_statique and rec.coefficient_statique:
                rec.theoretical_test_load_statique = rec.autorised_cmu_statique * rec.coefficient_statique
    
    @api.depends('coefficient_dynamique', 'autorised_cmu_dynamique')
    def _compute_theoretical_test_load_dynamique(self):
        for rec in self:
            if rec.autorised_cmu_dynamique and rec.coefficient_dynamique:
                rec.theoretical_test_load_dynamique = rec.autorised_cmu_dynamique * rec.coefficient_dynamique
    
    @api.onchange('inspection_type', 'verification_type')
    def onchange_levage_vp(self):
        if self.inspection_type == 'levage' and self.verification_type=='VP':
            self.comment_protection_dispositif = "Examen d'adéquation non concerné par la vérification périodique"
            self.comment_assembly_exam = "Examen de montage et d'installation non concerné par la vérification périodique"
            self.comment_epreuve_statique = "Epreuve statique non concerné par la vérification périodique"
            self.comment_epreuve_dynamique = "Epreuve dynamique non concerné par la vérification périodique"
        else:
            self.comment_protection_dispositif = ""
            self.comment_assembly_exam = ""
            self.comment_epreuve_statique = ""
            self.comment_epreuve_dynamique = ""
        
    @api.depends('characteristic_suspended_platform_ids', 'inspection_type', 'installation_type')
    def _compute_inspected_installation_number(self):
        for rec in self:
            if rec.inspection_type and rec.installation_type in ['PSE', 'PSM', 'PWM']:
                rec.inspected_installation_number = len(rec.characteristic_suspended_platform_ids)
    
    @api.depends('scaffolding_mark_ids', 'scaffolding_mark_ids.inspected_surface')
    def _compute_inspected_surface(self):
        for rec in self:
            if rec.scaffolding_mark_ids:
                rec.inspected_scaffolding_surface = sum(rec.scaffolding_mark_ids.mapped('inspected_surface'))
            
