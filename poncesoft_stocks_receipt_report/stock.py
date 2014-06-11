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
        'date_exit': fields.datetime('Fecha/Hora Autorizacion', help='Representa la Fecha y Hora en que Salio la Mercancia'),
        'placa': fields.char('Placa', size=256),
        'conductor': fields.char('Conductor', size=256),
        'notes_exit': fields.text('Observaciones'),
        'register_exit': fields.boolean('Salida Registrada', help='Registro de la salida de Mercancia'),
        }

    def print_receipt_report(self, cr, uid, ids, context=None):
        result = {
            'type': 'ir.actions.report.xml',
            'report_name': 'Autorizacion_de_Mercancia',
            'datas': {
                        'model' : 'stock.picking.out',
                        'ids'   : ids,
                        },
            } 
        
        return result

    def copy(self, cr, uid, id, default=None, context=None):
        if not default:
            default = {}
        default.update({
                        'date_exit': False,
                        'placa': False,
                        'conductor': False,
                        'notes_exit': False,
                        'register_exit': False,
                        })
        return super(stock_picking, self).copy(cr, uid, id, default, context=context)

stock_picking()


# STOCK PICKING IN
class stock_picking_in(osv.osv):
    _inherit = "stock.picking.in"
    _columns = {
        'date_exit': fields.datetime('Fecha/Hora Autorizacion', help='Representa la Fecha y Hora en que Salio la Mercancia'),
        'placa': fields.char('Placa', size=256, required=False),
        'conductor': fields.char('Conductor', size=256, required=False),
        'notes_exit': fields.text('Observaciones'),
        'register_exit': fields.boolean('Salida Registrada', help='Registro de la salida de Mercancia'),
        }

    def print_receipt_report(self, cr, uid, ids, context=None):
        result = {
            'type': 'ir.actions.report.xml',
            'report_name': 'Autorizacion_de_Mercancia',
            'datas': {
                        'model' : 'stock.picking.out',
                        'ids'   : ids,
                        },
            } 
        
        return result

    def copy(self, cr, uid, id, default=None, context=None):
        if not default:
            default = {}
        default.update({
                        'date_exit': False,
                        'placa': False,
                        'conductor': False,
                        'notes_exit': False,
                        'register_exit': False,
                        })
        return super(stock_picking_in, self).copy(cr, uid, id, default, context=context)

stock_picking_in()

# STOCK PICKING OUT
class stock_picking_out(osv.osv):
    _inherit = "stock.picking.out"
    _columns = {
        'date_exit': fields.datetime('Fecha/Hora Autorizacion', help='Representa la Fecha y Hora en que Salio la Mercancia'),
        'placa': fields.char('Placa', size=256, required=False),
        'conductor': fields.char('Conductor', size=256, required=False),
        'notes_exit': fields.text('Observaciones'),
        'register_exit': fields.boolean('Salida Registrada', help='Registro de la salida de Mercancia'),
        }

    def print_receipt_report(self, cr, uid, ids, context=None):
        result = {
            'type': 'ir.actions.report.xml',
            'report_name': 'Autorizacion_de_Mercancia',
            'datas': {
                        'model' : 'stock.picking.out',
                        'ids'   : ids,
                        },
            } 
        
        return result

    def copy(self, cr, uid, id, default=None, context=None):
        if not default:
            default = {}
        default.update({
                        'date_exit': False,
                        'placa': False,
                        'conductor': False,
                        'notes_exit': False,
                        'register_exit': False,
                        })
        return super(stock_picking_out, self).copy(cr, uid, id, default, context=context)
        
stock_picking_out()