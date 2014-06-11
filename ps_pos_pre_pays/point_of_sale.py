# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution    
#    Copyright (C) 2004-2010 Tiny SPRL (http://tiny.be). All Rights Reserved
#    
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see http://www.gnu.org/licenses/.
#
#
#
#    info skype: german_442 email: (german.ponce@hesatecnica.com)
############################################################################
#    Coded by: german_442 email: (german_442@hotmail.com)
#
##############################################################################

from osv import osv, fields
import time
from datetime import datetime, date
import decimal_precision as dp
from openerp import netsvc
from openerp.tools.translate import _
from openerp import SUPERUSER_ID

## CREANDO UN WIZARD PARA PAGOS ####
class pre_make_payment(osv.osv_memory):
    _name = 'pre.make.payment'
    _description = 'Pagos para los Apartados'

    def check(self, cr, uid, ids, context=None):
        """Check the order:
        if the order is not paid: continue payment,
        if the order is paid print ticket.
        """
        active_ids = context.get('active_ids', False)
        pos_obj = self.pool.get('pos.order')
        ### SUPER AL METODO DE PAGO PARA VALIDAR QUE NO SE VENDAN PRODUCTOS 
        ### CON UN COSTO MENOS AL ULTIMO PRECIO DE COMPRA O CATALOGO DE REMATES A MENOS QUE ESTEN AUTORIZADOS
       
        context = context or {}
        order_obj = self.pool.get('pos.order')
        obj_partner = self.pool.get('res.partner')
        active_id = context and context.get('active_id', False)

        order = order_obj.browse(cr, uid, active_id, context=context)
        amount = order.amount_total - order.amount_paid
        data = self.read(cr, uid, ids, context=context)[0]
        # this is probably a problem of osv_memory as it's not compatible with normal OSV's
        data['journal'] = data['journal_id'][0]

        if amount != 0.0:

            order_obj.add_payment(cr, uid, active_id, data, context=context)

        if order_obj.test_paid(cr, uid, [active_id], context=None):
            order_obj.action_paid(cr, SUPERUSER_ID, [active_id], context=None)
            value = {
            'type': 'ir.actions.report.xml',
            'report_name': 'Ticket',
            'datas': {
                        'model' : 'pos.order',
                        'ids'   : [active_id],
                        }
                    }
            
            return value
         ##self.print_report(cr, uid, ids, context=context)

        return self.launch_payment(cr, uid, ids, context=context)


    # def print_jasper_report(self, cr, uid, ids, context=None):
    #     active_id = context and context.get('active_id', False)
    #     print "############# ACTIVE IDS", active_id
    #     print "############# ACTIVE IDS", active_id
    #     print "############# ACTIVE IDS", active_id
    #     print "############# ACTIVE IDS", active_id
    #     ### Impresion del Nuevo Reporte de Ticket hecho en Jasper Reports
    #     value = {
    #         'type': 'ir.actions.report.xml',
    #         'report_name': 'Apartado',
    #         'datas': {
    #                     'model' : 'pos.order',
    #                     'ids'   : [active_id],
    #                     }
    #                 }

    #     return value

    def launch_payment(self, cr, uid, ids, context=None):
        return {
            'name': _('Payment'),
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'pre.make.payment',
            'view_id': False,
            'target': 'new',
            'views': False,
            'type': 'ir.actions.act_window',
            'context': context,
        }

    def _default_journal(self, cr, uid, context=None):
        if not context:
            context = {}
        session = False
        order_obj = self.pool.get('pos.order')
        active_id = context and context.get('active_id', False)
        if active_id:
            order = order_obj.browse(cr, uid, active_id, context=context)
            session = order.session_id
        if session:
            for journal in session.config_id.journal_ids:
                return journal.id
        return False

    def _default_amount(self, cr, uid, context=None):
        order_obj = self.pool.get('pos.order')
        active_ids = context and context.get('active_ids', False)
        if active_ids:
            for order in order_obj.browse(cr, uid, active_ids, context=None):
                result = order.amount_total - order.amount_paid
                return result
        return False

    _columns = {
        'journal_id' : fields.many2one('account.journal', 'Metodo de Pago', required=True),
        'amount': fields.float('Monto', digits=(16,2), required= True),
        'payment_name': fields.char('Referencia de Pago', size=32),
        'payment_date': fields.date('Fecha de Pago', required=True),
    }
    _defaults = {
        'journal_id' : _default_journal,
        'payment_date': lambda *a: datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'amount': _default_amount,
    }

pre_make_payment()

class pos_order(osv.osv):
    _name = 'pos.order'
    _inherit ='pos.order'
    _columns = {
        'partner_id':fields.many2one('res.partner', 'Cliente', required=False), 
        }

    _default = {
        }

    ### IMPRESION DEL TICKET HECHO EN JASPER REPORTS
    def print_jasper_report(self, cr, uid, ids, context=None):
        ### Impresion del Nuevo Reporte de Ticket hecho en Jasper Reports
        value = {
            'type': 'ir.actions.report.xml',
            'report_name': 'Ticket',
            'datas': {
                        'model' : 'pos.order',
                        'ids'   : ids,
                        }
                    }

        return value