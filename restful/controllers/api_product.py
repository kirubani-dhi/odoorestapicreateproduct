# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import http
from odoo.http import request
import logging
_logger = logging.getLogger(__name__)

class ProductApiController(http.Controller):

    # Access token get specified user
    def get_access_token(self,res_user_obj):    
        return [j.token for i in res_user_obj for j in i.token_ids]
    
    # Product Create Logic   
    @http.route('/api/product_create', type='json', auth="public")
    def producte_create(self, **kw):
        access_token = kw.get("access_token")
        res_user_obj = request.env['res.users'].sudo().search([('id','=',request.env.context['uid'])])
        acs_token_ids = self.get_access_token(res_user_obj)
        print(acs_token_ids)
        if access_token in acs_token_ids:
            if kw.get("parameters"):
                # print(kw.get("pp"))
                for params in kw.get("parameters"):
                    default_code = params.get('default_code')
                    name = params.get('name')
                    sale_ok = params.get('sale_ok')
                    purchase_ok = params.get('purchase_ok')
                    prodct_type = params.get('type')
                    categ_id = params.get('categ_id')
                    list_price = params.get('list_price')
                    standard_price = params.get('standard_price')
                    invoice_policy = params.get('invoice_policy')
                    weight = params.get('weight')
                    volume = params.get('volume')
                    product_category_rec = request.env['product.category'].sudo().search([('name','=',categ_id)])
                    if not product_category_rec:
                        product_category_rec = request.env['product.category'].sudo().create({
                            'name':categ_id,
                            'property_cost_method':'standard',
                            'property_valuation':'manual_periodic'
                        })
                    product_search_obj = request.env['product.template'].sudo().search([('default_code','=',default_code)])
                    if not product_search_obj:
                        product_search_obj = request.env['product.template'].sudo().create({
                            'default_code': default_code,
                            'name':name,
                            'sale_ok':sale_ok,
                            'purchase_ok':purchase_ok,
                            'type':prodct_type,
                            'categ_id':product_category_rec.id,
                            'list_price':list_price,
                            'standard_price':standard_price,
                            'invoice_policy':invoice_policy,
                            'weight':weight,
                            'volume':volume
                        })
                    
                    if product_search_obj:
                        status = 'Product Created Successfully'
                    else:
                        status = 'Product Name already Exists'
                    
                return {"status": status}