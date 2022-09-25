# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import http
from odoo.http import request
import logging
_logger = logging.getLogger(__name__)

class SaleOrderApiController(http.Controller):
    
    # Sale Order Create Logic   
    @http.route('/api/sale_order_create', type='json', auth="public")
    def sale_order_create(self, **kw):
        # date_order = kw.get("date_order")
        if kw.get("parameters"):
            print(kw.get("parameters"))
            for params in kw.get("parameters"):
                partner_name = params.get('partner_id')
                user_name = params.get('user_id')
                payment_term_id = params.get('payment_term_id')
                picking_policy = params.get('picking_policy')
                partner_Rec = request.env['res.partner'].sudo().search([('name','=',partner_name)],limit=1)
                if not partner_Rec:
                    status = "Customer is not available"
                    return {"status": status}
                else:
                    partner_Rec.write({
                        "sync_from_so_api":True,
                        "contact_id":partner_name
                    })
                # User record exist or not 
                user_Rec = request.env['res.users'].sudo().search([('name','=',user_name)],limit=1)
                if not user_Rec:
                    user_Rec = request.env['res.users'].sudo().create({
                        'name':user_name,
                        'login':user_name,
                        'password':user_name
                    })
                # Payment Term record exist or not    
                payment_term_id_Rec = request.env['account.payment.term'].sudo().search([('name','=',payment_term_id)])
                if not payment_term_id_Rec:
                    payment_term_id_Rec = request.env['account.payment.term'].sudo().create({
                        'name':payment_term_id,
                    })
                   
                # Update sale order line values 
                order_line_ids = []
                for order in params.get('order_line'):
                    qty = order['product_uom_qty'] if order['product_uom_qty'] else 1
                    price_unit = order['price_unit'] if order['price_unit'] else 1
                    product_temp = request.env['product.template'].sudo().search([('name','=',order['product_id'])])
                    if not product_temp:
                        status = "Product is not available"
                        return {"status": status}
                    else:
                        product_temp.write({
                            "sync_from_so_api":True,
                            "product_id":order['product_id']})
                    _logger.info("*************Inside - Product Temp Rec***********")
                    _logger.info(product_temp)

                    if product_temp:
                        product_variant = request.env['product.product'].sudo().search([('product_tmpl_id','=',product_temp.id)])
                        if not product_variant:
                            product_variant = request.env['product.product'].sudo().create({
                                "default_code": order['product_id'],
                                "name": order['product_id'],
                                "product_id":order['product_id'],
                            })
                        _logger.info("*************Inside - Product Variant Rec***********")
                        _logger.info(product_variant)
                    
                    order_line_vals = {
                        'product_id': product_variant.id,
                        'name': product_variant.name,
                        'product_uom_qty': qty,
                        'price_unit': price_unit,
                    }
                    order_line_ids.append([0, 0, order_line_vals])
                # print("Order Line Ids:",order_line_ids)
                                
                # Create a Sale Order 
                sale_order_id = request.env['sale.order'].sudo().create({
                    'partner_id': partner_Rec.id,
                    'user_id':user_Rec.id,
                    'payment_term_id':payment_term_id_Rec.id,
                    'picking_policy':picking_policy,
                    # 'date_order':date_order,
                    'order_line':order_line_ids,
                    })
                # print("sale_order_id",sale_order_id)
                if sale_order_id:
                    status = 'Quotation/ Sale Order Created Successfully'
                
            return {"status": status}