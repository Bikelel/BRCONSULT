# -*- coding: utf-8 -*-
from collections import OrderedDict
from odoo.osv.expression import OR, AND
from operator import itemgetter
from odoo import fields, http, SUPERUSER_ID, _
from odoo.exceptions import AccessError, MissingError, ValidationError
from odoo.http import request
from odoo.addons.portal.controllers import portal
from odoo.addons.portal.controllers.portal import pager as portal_pager, get_records_pager
from odoo.addons.http_routing.models.ir_http import slug, unslug
from odoo.addons.portal.controllers.mail import _message_post_helper
import datetime
import base64
import json
from base64 import encode
from markupsafe import Markup
from odoo.tools import date_utils
from dateutil.relativedelta import relativedelta
from odoo.tools import groupby as groupbyelem
import logging
_logger = logging.getLogger(__name__)

class CustomerPortal(portal.CustomerPortal):
    
    def _prepare_home_portal_values(self, counters):
        values = super()._prepare_home_portal_values(counters)
        partner = request.env.user.partner_id

        Prestation = request.env['prestation.prestation']
        if 'prestation_count' in counters:
            values['prestation_count'] = Prestation.search_count(self._prepare_prestations_domain(partner)) \
                if Prestation.check_access_rights('read', raise_exception=False) else 0
        if 'prestation_count_history' in counters:
            values['prestation_count_history'] = Prestation.search_count(self._prepare_prestations_domain_history(partner)) \
                if Prestation.check_access_rights('read', raise_exception=False) else 0
        return values
    
    def _prepare_prestations_domain(self, partner):
        domain = [('is_report_sent', '=', True)]
        if request.env.user.has_group('base.group_portal'):
            if not partner.is_mentor:
                domain += [('partner_id', 'child_of', [partner.commercial_partner_id.id]), ('partner_archive', '=', False)]
            else:
                domain += [('mentor_id', 'child_of', [partner.commercial_partner_id.id]), ('mentor_archive', '=', False)]
        return domain
    
    def _prepare_prestations_domain_history(self, partner):
        domain = [('is_report_sent', '=', True)]
        if request.env.user.has_group('base.group_portal'):
            if not partner.is_mentor:
                domain += [('partner_id', 'child_of', [partner.commercial_partner_id.id]), ('partner_archive', '=', True)]
            else:
                domain += [('mentor_id', 'child_of', [partner.commercial_partner_id.id]), ('mentor_archive', '=', True)]
        return domain
    
    def _get_prestation_searchbar_sortings(self):
        return {
            'verification_date': {'label': _('Date de v??rification'), 'order': 'verification_date desc'},
            'name': {'label': _('N?? Rapport'), 'order': 'name'},
        }
    
    def _get_prestation_searchbar_inputs(self):
        values = {
            'content': {'input': 'content', 'label': Markup(_('Search <span class="nolabel"> (in Content)</span>')), 'order': 1},
        }
        return dict(sorted(values.items(), key=lambda item: item[1]["order"]))
    
    def _get_prestation_search_domain(self, search_in, search):
        search_domain = []
        if search_in in ('content'):
            search_domain.append(['|',('name', 'ilike', search), ('site_address', 'ilike', search)])
        return OR(search_domain)

    
    @http.route(['/my/prestations', '/my/prestations/page/<int:page>'], type='http', auth="user", website=True)
    def portal_my_prestations(self, page=1, sortby=None, filterby=None, search=None, search_in='content', groupby=None, **kw):
        values = self._prepare_portal_layout_values()
        searchbar_sortings = self._get_prestation_searchbar_sortings()
        searchbar_inputs = self._get_prestation_searchbar_inputs()
        #searchbar_groupby = self._task_get_searchbar_groupby()
        today = fields.Date.today()
        quarter_start, quarter_end = date_utils.get_quarter(today)
        last_week = today + relativedelta(weeks=-1)
        last_month = today + relativedelta(months=-1)
        last_year = today + relativedelta(years=-1)
        next_three_month = today + relativedelta(months=3)
        next_six_month = today + relativedelta(months=6)
        next_twelve_month = today + relativedelta(months=12)
        searchbar_filters = {
            'all': {'label': _('Tous'), 'domain': []},
            'b_favorable_opinion': {'label': _('Avis favorable'), 'domain': [('opinion', '=', 'favorable_opinion')]},
            'b_opinion_with_observation': {'label': _('Avis favorable avec observation(s)'), 'domain': [('opinion', '=', 'opinion_with_observation')]},
            'b_defavorable_opinion': {'label': _('Avis defavorable'), 'domain': [('opinion', 'in', ('mixte', 'defavorable_opinion') )]},
            'month': {'label': ('Ce mois'), 'domain': [('date', '>=', date_utils.start_of(today, 'month')), ('date', '<=', date_utils.end_of(today, 'month'))]},
            
            'quarter': {'label': ('Ce trimestre'), 'domain': [('date', '>=', quarter_start), ('date', '<=', quarter_end)]},
            'year': {'label': ('Cette ann??e'), 'domain': [('date', '>=', date_utils.start_of(today, 'year')), ('date', '<=', date_utils.end_of(today, 'year'))]},
            'last_month': {'label': ('Le mois dernier'), 'domain': [('date', '>=', date_utils.start_of(last_month, 'month')), ('date', '<=', date_utils.end_of(last_month, 'month'))]},
            'last_year': {'label': ("L'ann??e derni??re year"), 'domain': [('date', '>=', date_utils.start_of(last_year, 'year')), ('date', '<=', date_utils.end_of(last_year, 'year'))]}
        }
        partner = request.env.user.partner_id
        user = request.env.user
        Prestation = request.env['prestation.prestation']

        domain = self._prepare_prestations_domain(partner)
        
        # default sortby order
        if not sortby:
            sortby = 'verification_date'
        sort_order = searchbar_sortings[sortby]['order']
        
        # default filter by value
        if not filterby:
            filterby = 'all'
        domain += searchbar_filters.get(filterby, searchbar_filters.get('all'))['domain']
        
        # search
        if search and search_in:
            domain += self._get_prestation_search_domain(search_in, search)

        # count for pager
        prestation_count = Prestation.search_count(domain)
        count_favorable_opinion = Prestation.search_count(domain + [('opinion', '=', 'favorable_opinion')])
        count_opinion_with_observation = Prestation.search_count(domain + [('opinion', '=', 'opinion_with_observation')])
        count_defavorable_opinion = Prestation.search_count(domain + [('opinion', 'in', ('mixte', 'defavorable_opinion'))])
        # make pager
        pager = portal_pager(
            url="/my/prestations",
            url_args={'sortby': sortby},
            total=prestation_count,
            page=page,
            step=self._items_per_page
        )
        # search the count to display, according to the pager data
        prestations = Prestation.search(domain, order=sort_order, limit=self._items_per_page, offset=pager['offset'])
        request.session['my_prestations_history'] = prestations.ids[:100]

        values.update({
            'prestations': prestations.sudo(),
            'page_name': 'prestation',
            'pager': pager,
            'default_url': '/my/prestations',
            'searchbar_sortings': searchbar_sortings,
            'sortby': sortby,
            #'searchbar_groupby' : searchbar_groupby,
            'searchbar_inputs' : searchbar_inputs,
            'search_in' :search_in,
            'search' : search,
            'searchbar_filters': OrderedDict(sorted(searchbar_filters.items())),
            'filterby': filterby,
            #'groupby': groupby,
            'user_id': user,
            'prestation_count': prestation_count,
            'count_favorable_opinion': count_favorable_opinion,
            'count_opinion_with_observation': count_opinion_with_observation,
            'count_defavorable_opinion': count_defavorable_opinion,
        })
        return request.render("website_brconsult.portal_my_prestations", values)
    
    @http.route(['/my/prestation/<int:prestation_id>'], type='http', auth="user", website=True)
    def portal_prestation_page(self, prestation_id, report_type=None, access_token=None, message=False, download=False, **kw):
        user = request.env.user
        try:
            prestation_sudo = self._document_check_access('prestation.prestation', prestation_id, access_token=access_token)
        except (AccessError, MissingError):
            return request.redirect('/my')

        if report_type in ('html', 'pdf', 'text'):
            return self._show_report(model=prestation_sudo, report_type=report_type, report_ref='br_consult.action_report_prestation', download=download)

        values = {
            'prestation': prestation_sudo,
            'message': message,
            'token': access_token,
            'bootstrap_formatting': True,
            'partner_id': prestation_sudo.partner_id.id,
            'report_type': 'html',
            'user_id': user
        }
        if prestation_sudo.company_id:
            values['res_company'] = prestation_sudo.company_id
        history = request.session.get('my_prestations_history', [])
        values.update(get_records_pager(history, prestation_sudo))
        return request.render('website_brconsult.prestation_portal_template', values)
    
    @http.route(['/my/prestation/<int:prestation_id>/edit'], auth='user', website=True)
    def edit_prestation_form(self, prestation_id, access_token=None, **kw):
        user = request.env.user
        try:
            prestation_sudo = self._document_check_access('prestation.prestation', prestation_id, access_token=access_token)
        except (AccessError, MissingError):
            return request.redirect('/my')

        values = {
            'prestation': prestation_sudo,
            'token': access_token,
            'bootstrap_formatting': True,
            'partner_id': prestation_sudo.partner_id.id,
            'user_id': user
        }
        if prestation_sudo.company_id:
            values['res_company'] = prestation_sudo.company_id
        history = request.session.get('my_prestations_history', [])
        values.update(get_records_pager(history, prestation_sudo))
        return request.render("website_brconsult.edit_prestation_page", values)
    
    def update_constat_line(self, constat, photo1, photo2, state, date):

        if date:
            constat.update({'date': datetime.datetime.strptime(date, '%d/%m/%Y')})
        if photo1:
            name = photo1.filename
            photo1_file = photo1
            photo1_attachment = photo1_file.read()
            constat.update({'photo_after_1': base64.b64encode(photo1_attachment)})
            
            
        if photo2:
            name = photo2.filename
            photo2_file = photo2
            photo2_attachment = photo2_file.read()
            constat.update({'photo_after_2': base64.b64encode(photo2_attachment)})
        if state:
            constat.update({'state': state})
        
    @http.route(['/my/prestation/confirm_edit'], type='http', auth="user", website=True, methods=['POST'])
    def portal_prestation_confirm_edit(self, **post):
        user = request.env.user
        partner = request.env.user.partner_id
        prestation_id = post.get('prestation_id')
        comment_mentor = post.get('comment_mentor')
        prestation_id = request.env['prestation.prestation'].sudo().browse(int(prestation_id))
        prestation_id.update({'comment_mentor': comment_mentor})
        #Examen d???ad??quation
        for constat in prestation_id.constat_adequacy_exam_ids:
            photo1 = post.get('photo1_adequacy_exam_' + str(constat.id))
            photo2 = post.get('photo2_adequacy_exam_' + str(constat.id))
            state = post.get('state_adequacy_exam_' + str(constat.id))
            date = post.get('date_adequacy_exam_' + str(constat.id))
            self.update_constat_line(constat, photo1, photo2, state, date)
        
        # Examen de montage et d'exploitation
        for constat in prestation_id.constat_assembly_exam_ids:
            photo1 = post.get('photo1_assembly_exam_' + str(constat.id))
            photo2 = post.get('photo2_assembly_exam_' + str(constat.id))
            state = post.get('state_assembly_exam_' + str(constat.id))
            date = post.get('date_assembly_exam_' + str(constat.id))
            self.update_constat_line(constat, photo1, photo2, state, date)
        
        # Examen de l'etat de conservation
        for constat in prestation_id.constat_conservation_state_exam_ids:
            photo1 = post.get('photo1_conservation_state_exam_' + str(constat.id))
            photo2 = post.get('photo2_conservation_state_exam_' + str(constat.id))
            state = post.get('state_conservation_state_exam_' + str(constat.id))
            date = post.get('date_conservation_state_exam_' + str(constat.id))
            self.update_constat_line(constat, photo1, photo2, state, date)
        
        # Examen de bon fonctionnement
        for constat in prestation_id.constat_good_functioning_exam_ids:
            photo1 = post.get('photo1_good_functioning_exam_' + str(constat.id))
            photo2 = post.get('photo2_good_functioning_exam_' + str(constat.id))
            state = post.get('state_good_functioning_exam_' + str(constat.id))
            date = post.get('date_good_functioning_exam_' + str(constat.id))
            self.update_constat_line(constat, photo1, photo2, state, date)
        
        # Epreuves statiques
        for constat in prestation_id.constat_epreuve_statique_ids:
            photo1 = post.get('photo1_epreuve_statique_' + str(constat.id))
            photo2 = post.get('photo2_epreuve_statique_' + str(constat.id))
            state = post.get('state_epreuve_statique_' + str(constat.id))
            date = post.get('date_epreuve_statique_' + str(constat.id))
            self.update_constat_line(constat, photo1, photo2, state, date)
            
         # Epreuves dynamiques
        for constat in prestation_id.constat_epreuve_dynamique_ids:
            photo1 = post.get('photo1_epreuve_dynamique_' + str(constat.id))
            photo2 = post.get('photo2_epreuve_dynamique_' + str(constat.id))
            state = post.get('state_epreuve_dynamique_' + str(constat.id))
            date = post.get('date_epreuve_dynamique_' + str(constat.id))
            self.update_constat_line(constat, photo1, photo2, state, date)
            
            
            
       
        return request.redirect(prestation_id.get_portal_url())
    
    @http.route(['/update_mentor/<prestation_id>'], auth='user', website=True)
    def update_mentor_form(self, prestation_id, **kw):
        _, prestation_id = unslug(prestation_id)
        user = request.env.user
        partner = request.env.user.partner_id
        mentors = request.env['res.partner'].sudo().search([('is_mentor', '=', True)])
        relaod_vals = {}
        prestation_id = request.env['prestation.prestation'].sudo().browse(prestation_id)
        if prestation_id.mentor_id:
            relaod_vals.update({'mentor_id': prestation_id.mentor_id})
        values = {'partner': partner,
                  'mentors': mentors,
                  'prestation': prestation_id,
                 }
        values['reload'] = relaod_vals
        return request.render("website_brconsult.update_mentor_page", values)
    
    @http.route(['/update_mentor/confirm'], type='http', auth="user", website=True, methods=['POST'])
    def portal_confirm_update_mentor(self, **post):
        user = request.env.user
        partner = request.env.user.partner_id
        mentor_id = post.get('monteur')
        prestation_id = post.get('prestation')
        mentor_id = request.env['res.partner'].sudo().browse(int(mentor_id))
        prestation_id = request.env['prestation.prestation'].sudo().browse(int(prestation_id))
        prestation_id.update({'mentor_id': mentor_id.id})
        template = request.env.ref('website_brconsult.email_notification_assign_mentor')
        if partner.email and mentor_id.email:
            email_values = {
                'email_from': partner.email,
                'email_to': mentor_id.email,
                #'email_cc': 'controlebr@brconsult.fr',
                'auto_delete': True,
                'recipient_ids': [],
                'partner_ids': [],
                'scheduled_date': False,}
            template.sudo().send_mail(prestation_id.id, force_send=True, email_values=email_values)
        return request.redirect(prestation_id.get_portal_url())
    
    @http.route(['/create_mentor/<prestation_id>'], auth='user', website=True)
    def create_mentor_form(self, prestation_id, **kw):
        _, prestation_id = unslug(prestation_id)
        user = request.env.user
        partner = request.env.user.partner_id
        mentors = request.env['res.partner'].sudo().search([('is_mentor', '=', True)])
        prestation_id = request.env['prestation.prestation'].sudo().browse(prestation_id)
        values = {'partner': partner,
                  'prestation': prestation_id,
                 }
        return request.render("website_brconsult.create_mentor_page", values)
    
    @http.route(['/create_mentor/confirm'], type='http', auth="user", website=True, methods=['POST'])
    def portal_confirm_create_mentor(self, **post):
        user = request.env.user
        partner = request.env.user.partner_id
        name = post.get('name')
        email = post.get('email')
        mobile = post.get('tel')
        siret = post.get('siret')
        prestation_id = post.get('prestation')
        vals = {'name': name,
                'email': email,
                'mobile': mobile,
                'is_mentor': True,
                'company_type': 'company'}
        mentor_id = request.env['res.partner'].sudo().create(vals)
        portal_wizard = request.env['portal.wizard'].sudo().with_context({
            'active_id': mentor_id.id,
            'active_ids': [mentor_id.id],
                         }).create({})
        portal_wizard.user_ids[0].action_grant_access()
        prestation_id = request.env['prestation.prestation'].sudo().browse(int(prestation_id))
        prestation_id.update({'mentor_id': mentor_id.id})
        template = request.env.ref('website_brconsult.email_notification_assign_mentor')
        if partner.email and mentor_id.email:
            email_values = {
                'email_from': partner.email,
                'email_to': mentor_id.email,
                #'email_cc': 'controlebr@brconsult.fr',
                'auto_delete': True,
                'recipient_ids': [],
                'partner_ids': [],
                'scheduled_date': False,}
            template.sudo().send_mail(prestation_id.id, force_send=True, email_values=email_values)
        return request.redirect(prestation_id.get_portal_url())
    
    @http.route(['/update_constat_line/<constat_id>'], auth='user', website=True)
    def update_constat_line_form(self, constat_id, **kw):
        _, constat_id = unslug(constat_id)
        user = request.env.user
        partner = request.env.user.partner_id
        relaod_vals = {}
        constat_id = request.env['prestation.constat'].sudo().browse(constat_id)
        values = {'constat': constat_id}
        return request.render("website_brconsult.update_constat_line_page", values)
    
    @http.route(['/update_constat_line/confirm'], type='http', auth="user", website=True, methods=['POST'])
    def portal_confirm_update_constat_line(self, **post):
        user = request.env.user
        partner = request.env.user.partner_id
        constat_id = post.get('constat')
        state = post.get('state')
        date_constat = post.get('date_constat')
        constat_id = request.env['prestation.constat'].sudo().browse(int(constat_id))
        constat_id.update({'state': state,
                           'date': datetime.datetime.strptime(date_constat, '%d/%m/%Y')})
        
        if post.get('photo1'):
            name = post.get('photo1').filename
            photo1_file = post.get('photo1')
            photo1_attachment = photo1_file.read()
            constat_id.update({'photo_after_1': base64.b64encode(photo1_attachment)})
        
        if post.get('photo2'):
            name = post.get('photo2').filename
            photo2_file = post.get('photo2')
            photo2_attachment = photo2_file.read()
            constat_id.update({'photo_after_2': base64.b64encode(photo2_attachment)})
            
        return request.redirect(constat_id.prestation_id.get_portal_url())
    
    @http.route(['/my/prestation/<int:prestation_id>/comment'], type='http', auth="user", website=True)
    def portal_report_comment(self, prestation_id, access_token=None, **kw):
        user = request.env.user
        partner = request.env.user.partner_id
        comment_mentor = kw.get('comment_mentor')
        try:
            prestation_sudo = self._document_check_access('prestation.prestation', prestation_id, access_token=access_token)
        except (AccessError, MissingError):
            return {'error': _('Invalide prestation.')}
        
        try:
            prestation_sudo.write({
                'comment_mentor': comment_mentor,
            })
        except (TypeError, binascii.Error) as e:
            return {'error': _('Invalid signature data.')}
            
        return {
            'force_refresh': True,
            'redirect_url': prestation_sudo.get_portal_url(query_string=query_string),
        }
        
    
    @http.route(['/my/prestation/<int:prestation_id>/accept'], type='json', auth="user", website=True)
    def portal_report_accept(self, prestation_id, access_token=None, name=None, signature=None, comment_mentor=None, **kw):
        user = request.env.user
        partner = request.env.user.partner_id
        # get from query string if not on json param
        access_token = access_token or request.httprequest.args.get('access_token')
        #comment_mentor = kw.get('comment_mentor')
        data_request = request.httprequest.args
        
                
        try:
            prestation_sudo = self._document_check_access('prestation.prestation', prestation_id, access_token=access_token)
        except (AccessError, MissingError):
            return {'error': _('Invalide prestation.')}

        if not signature:
            return {'error': _('Signature is missing.')}

        try:
            prestation_sudo.write({
                'signed_by': name,
                'signed_on': fields.Datetime.now(),
                'signature': signature,
            })
            request.env.cr.commit()
        except (TypeError, binascii.Error) as e:
            return {'error': _('Invalid signature data.')}

        pdf = request.env.ref('br_consult.action_report_reserve').with_user(SUPERUSER_ID)._render_qweb_pdf([prestation_sudo.id])[0]
        _message_post_helper(
            'prestation.prestation', prestation_sudo.id, _('Prestation sign?? par %s') % (name,),
            attachments=[('%s.pdf' % prestation_sudo.name, pdf)],
            **({'token': access_token} if access_token else {}))
        query_string = '&message=sign_ok'
        template = request.env.ref('website_brconsult.email_notification_validation_mentor')
        if partner.email and prestation_sudo.mentor_id and prestation_sudo.mentor_id.email and partner.is_mentor:
            email_values = {
                'email_from': prestation_sudo.mentor_id.email,
                'email_to': prestation_sudo.partner_id.email,
                #'email_cc': 'controlebr@brconsult.fr',
                'auto_delete': True,
                'recipient_ids': [],
                'partner_ids': [],
                'scheduled_date': False,}
            template.sudo().send_mail(prestation_sudo.id, force_send=True, email_values=email_values)
        return {
            'force_refresh': True,
            'redirect_url': prestation_sudo.get_portal_url(query_string=query_string),
        }
    
    @http.route(['/prestation/<int:prestation_id>/get_report_monteur'], type='http', auth='user', methods=['GET'], website=True)
    def get_report_monteur(self, prestation_id, **kw):     
        user = request.env.user
        prestation = request.env['prestation.prestation'].sudo().browse(prestation_id)
        if prestation:
            report_sudo = request.env.ref('br_consult.action_report_reserve').sudo()
            report = report_sudo._render_qweb_pdf([prestation.id])[0]
            #report = report_sudo.render_qweb_pdf([prestation.id])[0]
            pdfhttpheaders = [('Content-Type', 'application/pdf'), ('Content-Length', u'%s' % len(report))]
            return request.make_response(report, headers=pdfhttpheaders)
    
    @http.route(['/prestation/<int:prestation_id>/archive_report'], type='http', auth='user', methods=['GET'], website=True)
    def archive_report_monteur(self, prestation_id, **kw):      
        user = request.env.user
        prestation = request.env['prestation.prestation'].sudo().browse(prestation_id)
        if user.partner_id.is_mentor:
            prestation.update({'mentor_archive': True})
        else:
            prestation.update({'partner_archive': True})
            
        return request.redirect("/my/prestations")
    
    @http.route(['/prestation/<int:prestation_id>/unarchive_report'], type='http', auth='user', methods=['GET'], website=True)
    def unarchive_report_monteur(self, prestation_id, **kw):      
        user = request.env.user
        prestation = request.env['prestation.prestation'].sudo().browse(prestation_id)
        if user.partner_id.is_mentor:
            prestation.update({'mentor_archive': False})
        else:
            prestation.update({'partner_archive': False})
            
        return request.redirect("/my/prestations")
    

    @http.route(['/my/prestations/historique', '/my/prestations/historique/page/<int:page>'], type='http', auth="user", website=True)
    def portal_my_prestations_historique(self, page=1, sortby=None, filterby=None, search=None, search_in='content', groupby=None, **kw):
        values = self._prepare_portal_layout_values()
        searchbar_sortings = self._get_prestation_searchbar_sortings()
        searchbar_inputs = self._get_prestation_searchbar_inputs()
        searchbar_filters = {
            'all': {'label': _('Tous'), 'domain': []},
            'favorable_opinion': {'label': _('Avis favorable'), 'domain': [('opinion', '=', 'favorable_opinion')]},
            'opinion_with_observation': {'label': _('Avis favorable avec observation(s)'), 'domain': [('opinion', '=', 'opinion_with_observation')]},
            'defavorable_opinion': {'label': _('Avis defavorable'), 'domain': [('opinion', 'in', ('mixte', 'defavorable_opinion') )]},
        }
        partner = request.env.user.partner_id
        user = request.env.user
        Prestation = request.env['prestation.prestation']
        domain = self._prepare_prestations_domain_history(partner)

        # default sortby order
        if not sortby:
            sortby = 'verification_date'
        sort_order = searchbar_sortings[sortby]['order']
        
        # default filter by value
        if not filterby:
            filterby = 'all'
        domain += searchbar_filters.get(filterby, searchbar_filters.get('all'))['domain']
        
        # search
        if search and search_in:
            domain += self._get_prestation_search_domain(search_in, search)

        # count for pager
        prestation_count = Prestation.search_count(domain)
        # make pager
        pager = portal_pager(
            url="/my/prestations/historique",
            url_args={'sortby': sortby},
            total=prestation_count,
            page=page,
            step=self._items_per_page
        )
        # search the count to display, according to the pager data
        prestations = Prestation.search(domain, order=sort_order, limit=self._items_per_page, offset=pager['offset'])
        request.session['my_prestations_history'] = prestations.ids[:100]

        values.update({
            'prestations': prestations.sudo(),
            'page_name': 'prestation',
            'pager': pager,
            'default_url': '/my/prestations/historique',
            'searchbar_sortings': searchbar_sortings,
            'sortby': sortby,
            #'searchbar_groupby' : searchbar_groupby,
            'searchbar_inputs' : searchbar_inputs,
            'search_in' :search_in,
            'search' : search,
            'searchbar_filters': OrderedDict(sorted(searchbar_filters.items())),
            'filterby': filterby,
            #'groupby': groupby,
            'user_id': user,
        })
        return request.render("website_brconsult.portal_my_prestations", values)
    
    
    @http.route(['/my/prestations/statistique'], type='http', auth="user", website=True)
    def portal_my_prestations_statistique(self, page=1,**kw):
        values = self._prepare_portal_layout_values()
        
        partner = request.env.user.partner_id
        user = request.env.user
        Prestation = request.env['prestation.prestation']
        domain = self._prepare_prestations_domain(partner)

        # count for pager
        prestations = Prestation.search(domain)
        
        prestation_count = prestations.search_count(domain)
        count_favorable_opinion = prestations.search_count(domain + [('opinion', '=', 'favorable_opinion')])
        count_opinion_with_observation = prestations.search_count(domain+[('opinion', '=', 'opinion_with_observation')])
        count_defavorable_opinion = prestations.search_count(domain+[('opinion', 'in', ('mixte', 'defavorable_opinion'))])
        mentors = prestations.mapped('mentor_id')

        vals_mentor_avis = []
        for mentor in mentors:
            vals_mentor_avis.append({'mentor': mentor,
                                     'count_favorable_opinion': prestations.search_count(domain+[('opinion', '=', 'favorable_opinion'), ('mentor_id', '=', mentor.id)]),
                                     'count_opinion_with_observation': prestations.search_count(domain+[('opinion', '=', 'opinion_with_observation'), ('mentor_id', '=', mentor.id)]),
                                     'count_defavorable_opinion': prestations.search_count(domain+[('opinion', 'in', ('mixte', 'defavorable_opinion')), ('mentor_id', '=', mentor.id)]),
                                     
                                    })
        prestation_without_mentor = prestations.search(domain+[('mentor_id', '=', False)])
        vals_prestation_without_mentor = {}
        if prestation_without_mentor:
            vals_prestation_without_mentor = {'mentor': 'no',
                                             'count_favorable_opinion': prestation_without_mentor.search_count(domain+[('mentor_id', '=', False),('opinion', '=', 'favorable_opinion')]),
                                             'count_opinion_with_observation': prestation_without_mentor.search_count(domain+[('mentor_id', '=', False),('opinion', '=', 'opinion_with_observation')]),
                                             'count_defavorable_opinion': prestation_without_mentor.search_count(domain+[('mentor_id', '=', False),('opinion', 'in', ('mixte', 'defavorable_opinion'))]),
                                    }
        # Cat??gorie point de v??rification
        constats = request.env['prestation.constat'].search([('prestation_id', 'in', prestations.ids)])
        verifications_point = request.env['prestation.constat'].search([('prestation_id', 'in', prestations.ids)]).mapped('verification_point_id')
        
        vals_verifications_point = []
        for verification_point in verifications_point:
            vals_verifications_point.append({'verification_point': verification_point,
                                             'count_verification_point': constats.search_count([('verification_point_id', '=', verification_point.id)])})
            
        inspected_scaffolding_surface = sum(prestations.search(domain+[('inspection_type', '=', 'echafaudage')]).mapped('inspected_scaffolding_surface'))
        
        inspected_installation_number = sum(prestations.search(domain+[('inspection_type', '=', 'levage')]).mapped('inspected_installation_number'))
        
        vals_report_by_year = []
        years = prestations.mapped('year_prestation')
        years = list(set(years))
        _logger.info("########### years %s", years)
        for year in years:
            vals_report_by_year.append({'year': year,
                                        'nb_report': prestations.search_count(domain+[('year_prestation', '=', year)]),
                                        'inspected_scaffolding_surface': sum(prestations.search(domain+[('inspection_type', '=', 'echafaudage'), ('year_prestation', '=', year)]).mapped('inspected_scaffolding_surface')),
                                        'inspected_installation_number': sum(prestations.search(domain+[('inspection_type', '=', 'levage'), ('year_prestation', '=', year)]).mapped('inspected_installation_number'))
                                       
                                       })
            

            

        values.update({
            'prestations': prestations.sudo(),
            'page_name': 'prestation_statistique',
            'default_url': '/my/prestations/statistique',
            'user_id': user,
            'prestation_count': prestation_count,
            'count_favorable_opinion': count_favorable_opinion,
            'count_opinion_with_observation': count_opinion_with_observation,
            'count_defavorable_opinion': count_defavorable_opinion,
            'vals_mentor_avis': vals_mentor_avis,
            'mentors': mentors,
            'vals_prestation_without_mentor':vals_prestation_without_mentor,
            'constats': constats,
            'verifications_point': verifications_point,
            'vals_verifications_point': vals_verifications_point,
            'inspected_scaffolding_surface': inspected_scaffolding_surface,
            'inspected_installation_number': inspected_installation_number,
            'vals_report_by_year': vals_report_by_year,
            
        })
        return request.render("website_brconsult.portal_my_prestations_statistique", values)