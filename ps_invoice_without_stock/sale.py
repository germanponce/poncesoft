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
import netsvc
import pooler
from tools.translate import _
import decimal_precision as dp
from osv.orm import browse_record, browse_null
import time
from datetime import datetime, date
from openerp import SUPERUSER_ID

# Agregamos manejar una secuencia por cada tienda para controlar viajes 
class sale_order(osv.osv):
    _name = "sale.order"
    _inherit = "sale.order"
    
    _columns = {
        'invoice_without_stock': fields.boolean('Facturar sin Stock', required=False), 
        }

    def action_invoice_create(self, cr, uid, ids, grouped=False, states=None, date_invoice = False, context=None):
        res = super(sale_order, self).action_invoice_create(cr, uid, ids, grouped=False, states=None, date_invoice = False, context=None)
        for order in self.browse(cr, uid, ids, context=context):
            lineas_sin_stock = 0
            productos = ''
            shop_obj = self.pool.get('sale.shop')
            sale_ids = shop_obj.search(cr, SUPERUSER_ID, [])
            for linea in order.order_line:      
                ## Verificar Existencias y añadirlo a productos
                if linea.product_id.qty_available <= 0.0:
                    lineas_sin_stock += 1
                    productos = productos +' | '+linea.product_id.name
            if lineas_sin_stock > 0:
                if order.invoice_without_stock == False:
                    raise osv.except_osv(
                            _('Error !'),
                            _('Uno de los Productos no Cuenta con Existencia %s.\n Para Continuar Pulse Autorizar Venta \
                                El usuario que que autorizara debe estar en el Grupo [Facturacion Especial]') % productos)
        return res
    
    def action_button_confirm(self, cr, uid, ids, context=None):
        res = super(sale_order, self).action_button_confirm(cr, uid, ids, context=None)
        for order in self.browse(cr, uid, ids, context=context):
            lineas_sin_stock = 0
            productos = ''
            shop_obj = self.pool.get('sale.shop')
            sale_ids = shop_obj.search(cr, SUPERUSER_ID, [])
            for linea in order.order_line:      
                ## Verificar Existencias y añadirlo a productos
                if linea.product_id.qty_available <= 0.0:
                    lineas_sin_stock += 1
                    productos = productos +' | '+linea.product_id.name
            if lineas_sin_stock > 0:
                if order.invoice_without_stock == False:
                    raise osv.except_osv(
                            _('Error !'),
                            _('Uno de los Productos no Cuenta con Existencia %s.\n Para Continuar Pulse Autorizar Venta \
                                El usuario que que autorizara debe estar en el Grupo [Facturacion Especial]') % productos)
        return  res
sale_order()

### CREACION DEL WIZARD PARA AUTORIZAR FACTURA
class sale_order_invoice_stock(osv.osv_memory):
    _name = 'sale.order.invoice.stock'
    _description = 'Asistente para Facturacion sin Stock'
    _columns = {
    'password' : fields.char('Contraseña del Usuario', size=128, required=True),
    }
    _defaults = {  

        }

    def auth(self, cr, uid, ids, context=None):
        active_ids = context.get('active_ids', False)
        password = self.browse(cr, SUPERUSER_ID, ids, context=None)[0].password
        group_obj = self.pool.get('res.groups')
        group_id = group_obj.search(cr, SUPERUSER_ID, [('name','=','Facturacion Especial')])
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
                    for sale in sale_order_obj.browse(cr, SUPERUSER_ID, active_ids, context=None):
                        ret = sale.write({'invoice_without_stock':True})
                return ret
            else:
                raise osv.except_osv(
                        _('Error !'),
                        _('La Contraseña es Incorrecta o el Usuario no tiene Permisos.\n Consulte a su Administrador y Verifique \
                            que el usuario se encuentra en el Grupo [Facturacion Especial]'))
        else:
            raise osv.except_osv(
                    _('Error !'),
                    _('La Contraseña es Incorrecta o el Usuario no tiene Permisos.\n Consulte a su Administrador y Verifique \
                        que el usuario se encuentra en el Grupo [Facturacion Especial]'))
        return {'type' : 'ir.actions.act_window_close' }

sale_order_invoice_stock()
