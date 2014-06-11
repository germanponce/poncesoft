# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
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

from openerp.osv import fields, osv, orm
from datetime import time, datetime
from tools.translate import _
from openerp import tools

class stock_exit_products(osv.osv_memory):
    _name = 'stock.exit.products'
    _description = 'Autorizacion de Salida de Mercancia'
    _columns = {
    'date_exit': fields.datetime('Fecha/Hora Autorizacion', help='Representa la Fecha y Hora en que Salio la Mercancia'),
    'placa': fields.char('Placa', size=256, required=True),
    'conductor': fields.char('Conductor', size=256, required=True),
    'notes_exit': fields.text('Observaciones'),
    }
    _defaults = {  
    'date_exit':lambda *a: datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        }

    def exit_register(self, cr, uid, ids, context=None):
        active_ids = context.get('active_ids', False)
        stock_obj = self.pool.get('stock.picking.out')
        for rec in self.browse(cr, uid, ids, context=None):
            for stock in stock_obj.browse(cr, uid, active_ids, context=None):
                stock.write({
                    'date_exit': rec.date_exit,
                    'placa': rec.placa,
                    'conductor': rec.conductor,
                    'notes_exit': rec.notes_exit,
                    'register_exit': True,
                    })
        result = {
            'type': 'ir.actions.report.xml',
            'report_name': 'Autorizacion_de_Mercancia',
            'datas': {
                        'model' : 'stock.picking.out',
                        'ids'   : active_ids,
                        },
            }
        return result

stock_exit_products()