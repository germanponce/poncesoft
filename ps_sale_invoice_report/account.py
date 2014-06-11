# -*- encoding: utf-8 -*-
##############################################################################
#    
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2009 Tiny SPRL (<http://tiny.be>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.     
#
##############################################################################

from osv import osv, fields
import time
from datetime import datetime, date
import decimal_precision as dp
from openerp import netsvc


# STOCK PICKING
class account_invoice(osv.osv):
    _name = "account.invoice"
    _inherit ='account.invoice'
    _columns = {
        'sale_order_ids': fields.one2many('order.report.lines','account_id','Pedidos de Venta Relacionados'),
        }

    def print_jasper_report(self, cr, uid, ids, context=None):
        value = {
            'type': 'ir.actions.report.xml',
            'report_name': 'Factura_Detalle_Ventas',
            'datas': {
                        'model' : 'account.invoice',
                        'ids'   : ids,
                        }
                    }

        return value

account_invoice()

class order_report_lines(osv.osv):
    _name = 'order.report.lines'
    _description = 'Pedidos de Venta Origen'
    _rec_name = 'order_id' 
    _columns = {
        'account_id': fields.many2one('account.invoice', 'ID Ref'),
        'order_id': fields.many2one('sale.order','Origen del Pedido'),

    }
    _defaults = {  
        }
    _order = 'id' 
order_report_lines()

class sale_order(osv.osv):
    _name = "sale.order"
    _inherit = "sale.order"
    
    _columns = {
        }

    def action_invoice_create(self, cr, uid, ids, grouped=False, states=None, date_invoice = False, context=None):
        active_ids = ids
        res = super(sale_order, self).action_invoice_create(cr, uid, ids, grouped, states, date_invoice, context=None)
        account_invoice_obj = self.pool.get('account.invoice')
        for account in account_invoice_obj.browse(cr, uid, [res], context=None):
            order_ids = []
            if not account.sale_order_ids:
                for di in ids:
                    xline = (0,0,{
                        'order_id': di,
                        })
                    order_ids.append(xline)
                account.write({'sale_order_ids':[x for x in order_ids]})
        return res
        
sale_order()