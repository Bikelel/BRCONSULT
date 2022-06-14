# -*- coding: utf-8 -*-
from odoo import fields, http, SUPERUSER_ID, _
from odoo.exceptions import AccessError, MissingError, ValidationError
from odoo.http import request
from odoo.addons.portal.controllers import portal
from odoo.addons.portal.controllers.portal import pager as portal_pager, get_records_pager
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
            domain += [('partner_id', 'child_of', [partner.commercial_partner_id.id])]
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
        })
        return request.render("website_brconsult.portal_my_prestations", values)
    
    @http.route(['/my/prestation/<int:prestation_id>'], type='http', auth="public", website=True)
    def portal_prestation_page(self, prestation_id, report_type=None, access_token=None, message=False, download=False, **kw):
        _logger.info("##################")
        try:
            prestation_sudo = self._document_check_access('prestation.prestation', prestation_id, access_token=access_token)
        except (AccessError, MissingError):
            return request.redirect('/my')

        if report_type in ('html', 'pdf', 'text'):
            return self._show_report(model=prestation_sudo, report_type=report_type, report_ref='br_consult.action_report_prestation', download=download)

        # use sudo to allow accessing/viewing orders for public user
        # only if he knows the private token
        # Log only once a day
        if prestation_sudo:
            # store the date as a string in the session to allow serialization
            now = fields.Date.today().isoformat()
            session_obj_date = request.session.get('view_quote_%s' % prestation_sudo.id)
            if session_obj_date != now and request.env.user.share and access_token:
                request.session['view_quote_%s' % prestation_sudo.id] = now
                body = _('Report viewed by customer %s', prestation_sudo.partner_id.name)
                _message_post_helper(
                    "prestation.prestation",
                    prestation_sudo.id,
                    body,
                    token=order_sudo.access_token,
                    message_type="notification",
                    subtype_xmlid="mail.mt_note",
                    partner_ids=prestation_sudo.user_id.sudo().partner_id.ids,
                )

        values = {
            'prestation': prestation_sudo,
            'message': message,
            'token': access_token,
            'bootstrap_formatting': True,
            'partner_id': prestation_sudo.partner_id.id,
            'report_type': 'html',
        }
        if prestation_sudo.company_id:
            values['res_company'] = prestation_sudo.company_id

        history = request.session.get('my_prestations_history', [])

        values.update(get_records_pager(history, prestation_sudo))

        return request.render('website_brconsult.prestation_portal_template', values)