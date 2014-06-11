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
import dateutil
import dateutil.parser
from dateutil.relativedelta import relativedelta
from datetime import datetime, date
from tools.translate import _
from tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT, float_compare
import decimal_precision as dp
import netsvc
import openerp
import calendar
from openerp import SUPERUSER_ID

# Agregamos manejar una secuencia por cada tienda para controlar viajes 
class sale_order(osv.osv):
    _name = "sale.order"
    _inherit = "sale.order"
    _columns = {
    'exced_credit': fields.boolean('Limite de Credito Excedido'),
   # 'pricelist_id': fields.many2one('product.pricelist', 'Pricelist', required=True,states={'draft': [('readonly', False)], 'sent': [('readonly', False)]}, help="Pricelist for current sales order", domain=[('type','=','sale')], change_default=True),
    'global_discount': fields.float('Descuento Global (%)', digits_compute= dp.get_precision('Account'), required=False),
    }

    def get_current_instance(self, cr, uid, id):
        lines = self.browse(cr,uid,id)
        obj = None
        for i in lines:
            obj = i
        return obj

    def onchange_partner_id(self, cr, uid, ids, part, context=None):
        if not part:
            return {'value':{}}
        warning = {}
        title = False
        message = False
        partner = self.pool.get('res.partner').browse(cr, uid, part, context=context)
        title =  _("Informacion Financiera para %s") % partner.name
        this = self.get_current_instance(cr, uid, ids)
        message = " "
        warning = {
                'title': title,
                'message': message,
        }
        
        credit_exc = 0.0
        if partner.credit == 0:
            credit_exc == 0.0
        elif partner.credit > 0.0:
            credit_exc = partner.credit_limit - partner.credit
            if credit_exc < 0.0:
                credit_exc = credit_exc * (-1)

        account_voucher_obj = self.pool.get('account.voucher')
        account_voucher_ids = account_voucher_obj.search(cr, uid, [('partner_id','=',part)])
        date = ''
        for voucher in account_voucher_obj.browse(cr, uid, account_voucher_ids, context=context):
            if voucher.date > date:
                date = voucher.date
        if not account_voucher_ids:
            date = 'No se ah detectado Pago'
        result =  super(sale_order, self).onchange_partner_id(cr, uid, ids, part, context=context)
        cadena = "Total a Cobrar: $ " +  str('{:,}'.format(partner.credit)) +'   ' + '\nLimite de Credito: $ ' + str('{:,}'.format(partner.credit_limit)) + '   '+ '\nCredito Excedido: $ ' + str('{:,}'.format(credit_exc)) + '   ' + '\nFecha del Ultimo Pago: ' + date 
        warning['message'] = message + str(cadena)
        if partner.credit_limit < partner.credit:
            value_d = result.get('value',{})
            value_d['exced_credit']= True

            return {'value': value_d, 'warning':warning}

        return {'value': result.get('value',{})}
        


    def action_button_confirm(self, cr, uid, ids, context=None):
        res = super(sale_order, self).action_button_confirm(cr, uid, ids, context=None)
        for order in self.browse(cr, uid, ids, context=context):
            credit_exc = 0.0
            if order.partner_id.credit == 0:
                credit_exc == 0.0
            elif order.partner_id.credit > 0.0:
                credit_exc = order.partner_id.credit_limit - order.partner_id.credit
                if credit_exc < 0.0:
                    credit_exc = credit_exc * (-1)
            if order.partner_id.credit_limit < order.partner_id.credit:
                order.write({'exced_credit':True})
                raise osv.except_osv(
                        _('No se puede Confirmar !'),
                        _('El Cliente %s ah Excedido el Limite de Credito \n Para autorizar utilice el Asistende de Credito' % order.partner_id.name))
            future_credit = order.partner_id.credit + order.amount_total
            if order.partner_id.credit_limit < future_credit:
                order.write({'exced_credit':True})
            if order.partner_id.credit_limit < future_credit:
                raise osv.except_osv(
                        _('No se puede Confirmar !'),
                        _('El Cliente %s ah Excedido el Limite de Credito con esta Venta \n Para autorizar active la casilla Limite de Credito Excedido en la Pestaña Otra Informacion y  Utilice el Asistende de Credito' % order.partner_id.name))
            return  res
sale_order()


class sale_order_extend_credit(osv.osv_memory):
    _name = 'sale.order.extend.credit'
    _description = 'Asistente para Entender el Credito'
    _columns = {
    'partner_id': fields.many2one('res.partner', 'Cliente', readonly=True),
    'credit': fields.float('Total a Cobrar', digits=(12,2), readonly=True),
    'credit_limit': fields.float('Credito Concedito', digits=(12,2), readonly=True),
    'credit_extend': fields.float('Credito Nuevo', digits=(12,2), required=True, help='Indica el Nuevo Monto Autorizado de Credito, por defecto como sugerencia el Sistema Suma el Credito que Adeuda el Cliente + el monto del pedido de Venta' ),
    'password' : fields.char('Contraseña del Usuario', size=128, required=True),
    }

    def _get_partner(self, cr, uid, context=None):
        active_id = context.get('active_id', False)
        sale_obj = self.pool.get('sale.order')
        sale_br = sale_obj.browse(cr, uid, [active_id], context=None)[0]
        return sale_br.partner_id.id

    def _get_credit(self, cr, uid, context=None):
        active_id = context.get('active_id', False)
        sale_obj = self.pool.get('sale.order')
        sale_br = sale_obj.browse(cr, uid, [active_id], context=None)[0]
        return sale_br.partner_id.credit

    def _get_limit(self, cr, uid, context=None):
        active_id = context.get('active_id', False)
        sale_obj = self.pool.get('sale.order')
        sale_br = sale_obj.browse(cr, uid, [active_id], context=None)[0]
        return sale_br.partner_id.credit_limit

    def _get_credit_new(self, cr, uid, context=None):
        active_id = context.get('active_id', False)
        sale_obj = self.pool.get('sale.order')
        sale_br = sale_obj.browse(cr, uid, [active_id], context=None)[0]
        credit_extend = sale_br.partner_id.credit + sale_br.amount_total
        return credit_extend

    _defaults = {

    'partner_id': _get_partner,
    'credit': _get_credit,
    'credit_limit': _get_limit,
    'credit_extend': _get_credit_new,

        }

    def auth(self, cr, uid, ids, context=None):
        active_ids = context.get('active_ids', False)
        password = self.browse(cr, SUPERUSER_ID, ids, context=None)[0].password
        group_obj = self.pool.get('res.groups')
        group_id = group_obj.search(cr, SUPERUSER_ID, [('name','=','Ventas / Permisos Especiales')])
        users_obj = self.pool.get('res.users')
        user_list = []
        sale_order_obj = self.pool.get('sale.order')
        for group in group_obj.browse(cr, SUPERUSER_ID, group_id, context=None):
            for user in group.users:
                user_list.append(user.id)
        if user_list:
            user_ids = users_obj.search(cr, SUPERUSER_ID, [('password','=',password),('id','in',tuple(user_list))])
            if user_ids:
                if active_ids:
                    partner_obj = self.pool.get('res.partner')
                    for rec in self.browse(cr, uid, ids, context=None):
                        sale_order_obj.write(cr, uid, active_ids, {'exced_credit': False})
                        partner_obj.write(cr, uid, [rec.partner_id.id], {'credit_limit': rec.credit_extend})
                return {'type' : 'ir.actions.act_window_close' }
            else:
                raise osv.except_osv(
                        _('Error !'),
                        _('La Contraseña es Incorrecta o el Usuario no tiene Permisos.\n Consulte a su Administrador y Verifique \
                            que el usuario se encuentra en el Grupo [Ventas / Permisos Especiales]'))
        else:
            raise osv.except_osv(
                    _('Error !'),
                    _('La Contraseña es Incorrecta o el Usuario no tiene Permisos.\n Consulte a su Administrador y Verifique \
                        que el usuario se encuentra en el Grupo [Ventas / Permisos Especiales]'))
        return {'type' : 'ir.actions.act_window_close' }

sale_order_extend_credit()