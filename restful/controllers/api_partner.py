# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import http
from odoo.http import request
import logging
_logger = logging.getLogger(__name__)

class PrartnerApiController(http.Controller):

    # Partner Create Logic
    @http.route('/api/partner_create', type='json', auth="public")
    def partner_create(self, **kw):
        if kw.get("parameters"):
            # print(kw.get("pp"))
            for params in kw.get("parameters"):
                company_type = params.get('company_type')
                name = params.get('name')
                street = params.get('street')
                street2 = params.get('street2')
                city = params.get('city')
                state_name = params.get('state_id')
                zip = params.get('zip')
                country_name = params.get('country_id')
                vat = params.get('vat')
                phone = params.get('phone')
                email = params.get('email')
                website = params.get("website")
                
                country_Rec = request.env['res.country'].sudo().search([('name','=',country_name)])
                state_Rec = request.env['res.country.state'].sudo().search([('name','=',state_name)])
                partner_rec = request.env['res.partner'].sudo().search([('name','=',name)],limit=1)
                if not partner_rec:
                    partner_rec = request.env['res.partner'].sudo().create({
                        'name':name,
                        'company_type':company_type,
                        'street':street,
                        'street2':street2,
                        'city':city,
                        'state_id':state_Rec.id if state_Rec else False,
                        'zip':zip,
                        'country_id':country_Rec.id if country_Rec else False,
                        'vat':vat,
                        'phone':phone,
                        'email':email,
                        'website':website
                    })
                
                if partner_rec:
                    status = 'Partner Created Successfully'
                else:
                    status = 'Partner Name already Exists'
                
            return {"status": status}
        