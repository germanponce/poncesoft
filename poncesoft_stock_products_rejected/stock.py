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
class stock_picking(osv.osv):
    _name = "stock.picking"
    _inherit ='stock.picking'
    _columns = {
        'rejected_ids': fields.one2many('stock.rejected.lines', 'stock_id','Productos Averiados'),
        }

    _default = {
        }

    def _check_rejected(self, cr, uid, ids, context=None): 
        for rec in self.browse(cr, uid, ids, context=None):
            picking_line_obj = self.pool.get('stock.move')
            reject_obj = self.pool.get('stock.rejected.lines')
            if rec.rejected_ids:
                reject_qty = 0
                move_qty = 0
                for reject in rec.rejected_ids:
                    product_id = reject.product_id.id
                    reject_qty = reject.qty
                    reject_lines = reject_obj.search(cr, uid,[('stock_id','=',rec.id),('product_id','=',product_id)])
                    if len(reject_lines)>1:
                        reject_qty = 0
                        for rjl in reject_obj.browse(cr, uid, reject_lines, context=None):
                            reject_qty += rjl.qty
                    picking_lines = picking_line_obj.search(cr, uid, [('picking_id','=',rec.id),('product_id','=',product_id)])
                    if not picking_lines:
                        return False
                    for move in picking_line_obj.browse(cr, uid, picking_lines, context=None):
                        move_qty += move.product_qty
                    if move_qty >= reject_qty:
                        return True
                    else:
                        return False

        return True
    _constraints = [(_check_rejected, 'Error: La Cantidad que se agrego es superior a la Cantidad de Producto Recibida ó el Producto No existe como Linea de Entrada. \n Revisa las Pestaña Averias ó Contacte a su Administrador', ['rejected_ids']), ] 

    ## SUPER AL METODO COPIAR PARA BORRAR LINEAS DE AVERIAS

    def copy(self, cr, uid, id, default=None, context=None):
        if not default:
            default = {}
        default.update({
                        'rejected_ids': False, 
                        })
        return super(stock_picking, self).copy(cr, uid, id, default, context=context)

stock_picking()


# STOCK PICKING OUT
class stock_picking_in(osv.osv):
    _inherit = "stock.picking.in"
    _columns = {
        'rejected_ids': fields.one2many('stock.rejected.lines', 'stock_id','Productos Averiados'),
        }

    def _check_rejected(self, cr, uid, ids, context=None): 
        for rec in self.browse(cr, uid, ids, context=None):
            picking_line_obj = self.pool.get('stock.move')
            reject_obj = self.pool.get('stock.rejected.lines')
            if rec.rejected_ids:
                reject_qty = 0
                move_qty = 0
                for reject in rec.rejected_ids:
                    product_id = reject.product_id.id
                    reject_qty = reject.qty
                    reject_lines = reject_obj.search(cr, uid,[('stock_id','=',rec.id),('product_id','=',product_id)])
                    if len(reject_lines)>1:
                        reject_qty = 0
                        for rjl in reject_obj.browse(cr, uid, reject_lines, context=None):
                            reject_qty += rjl.qty
                    picking_lines = picking_line_obj.search(cr, uid, [('picking_id','=',rec.id),('product_id','=',product_id)])
                    if not picking_lines:
                        return False
                    for move in picking_line_obj.browse(cr, uid, picking_lines, context=None):
                        move_qty += move.product_qty
                    if move_qty >= reject_qty:
                        return True
                    else:
                        return False

        return True
    _constraints = [(_check_rejected, 'Error: La Cantidad que se agrego es superior a la Cantidad de Producto Recibida ó el Producto No existe como Linea de Entrada. \n Revisa las Pestaña Averias ó Contacte a su Administrador', ['rejected_ids']), ] 

    ## SUPER AL METODO COPIAR PARA BORRAR LINEAS DE AVERIAS

    def copy(self, cr, uid, id, default=None, context=None):
        if not default:
            default = {}
        default.update({
                        'rejected_ids': False, 
                        })
        return super(stock_picking_in, self).copy(cr, uid, id, default, context=context)

stock_picking_in()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
