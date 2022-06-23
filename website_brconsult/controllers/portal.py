# -*- coding: utf-8 -*-
from odoo import fields, http, SUPERUSER_ID, _
from odoo.exceptions import AccessError, MissingError, ValidationError
from odoo.http import request
from odoo.addons.portal.controllers import portal
from odoo.addons.portal.controllers.portal import pager as portal_pager, get_records_pager
from odoo.addons.http_routing.models.ir_http import slug, unslug
from odoo.addons.portal.controllers.mail import _message_post_helper
import datetime
import base64
from base64 import encode
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
        return values
    
    def _prepare_prestations_domain(self, partner):
        domain = [('is_report_sent', '=', True)]
        if request.env.user.has_group('base.group_portal'):
            if not partner.is_mentor:
                domain += [('partner_id', 'child_of', [partner.commercial_partner_id.id])]
            else:
                domain += [('mentor_id', 'child_of', [partner.commercial_partner_id.id]), ('mentor_archive', '=', False)]
                
        return domain
    
    def _get_sale_searchbar_sortings(self):
        return {
            'verification_date': {'label': _('Date de vérification'), 'order': 'verification_date desc'},
            'name': {'label': _('N° Rapport'), 'order': 'name'},
        }
    
    @http.route(['/my/prestations', '/my/prestations/page/<int:page>'], type='http', auth="user", website=True)
    def portal_my_prestations(self, page=1, sortby=None, **kw):
        values = self._prepare_portal_layout_values()
        partner = request.env.user.partner_id
        user = request.env.user
        Prestation = request.env['prestation.prestation']

        domain = self._prepare_prestations_domain(partner)

        searchbar_sortings = self._get_sale_searchbar_sortings()

        # default sortby order
        if not sortby:
            sortby = 'verification_date'
        sort_order = searchbar_sortings[sortby]['order']

        # count for pager
        prestation_count = Prestation.search_count(domain)
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
            'user_id': user,
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
#         if prestation_sudo:
#             # store the date as a string in the session to allow serialization
#             now = fields.Date.today().isoformat()
#             session_obj_date = request.session.get('view_quote_%s' % prestation_sudo.id)
#             if session_obj_date != now and request.env.user.share and access_token:
#                 request.session['view_quote_%s' % prestation_sudo.id] = now
#                 body = _('Report viewed by customer %s', prestation_sudo.partner_id.name)
#                 _message_post_helper(
#                     "prestation.prestation",
#                     prestation_sudo.id,
#                     body,
#                     token=prestation_sudo.access_token,
#                     message_type="notification",
#                     subtype_xmlid="mail.mt_note",
#                     partner_ids=prestation_sudo.user_id.sudo().partner_id.ids,
#                 )

        values = {
            'prestation': prestation_sudo,
            'message': message,
            'token': access_token,
            'bootstrap_formatting': True,
            'partner_id': prestation_sudo.partner_id.id,
            'report_type': 'html',
            'user_id': user,
            
        }
        if prestation_sudo.company_id:
            values['res_company'] = prestation_sudo.company_id

        history = request.session.get('my_prestations_history', [])

        values.update(get_records_pager(history, prestation_sudo))

        return request.render('website_brconsult.prestation_portal_template', values)
    
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
    
    @http.route(['/my/prestation/<int:prestation_id>/accept'], type='json', auth="user", website=True)
    def portal_report_accept(self, prestation_id, access_token=None, name=None, signature=None):
        user = request.env.user
        partner = request.env.user.partner_id
        # get from query string if not on json param
        access_token = access_token or request.httprequest.args.get('access_token')
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
            'prestation.prestation', prestation_sudo.id, _('Prestation signé par %s') % (name,),
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
    
    @http.route(['/prestation/<int:prestation_id>/archive_report_monteur'], type='http', auth='user', methods=['GET'], website=True)
    def archive_report_monteur(self, prestation_id, **kw):
       
        user = request.env.user
        prestation = request.env['prestation.prestation'].sudo().browse(prestation_id)
        prestation.update({'mentor_archive': True})
            
        return request.redirect("/my/prestations")
