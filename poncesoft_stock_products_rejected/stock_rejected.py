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

class stock_rejected_lines(osv.osv):
    _name = "stock.rejected.lines"
    _description = "Lineas Marcadas con Defectos en la Recepcion"
    _columns = {
    'stock_id': fields.many2one('stock.picking.in','Albaran'),
    'name': fields.char('No. Serie', size=128, help='Este Numero de Serie se obtiene al capturar el Producto', ),
    'date': fields.date('Fecha', required=True),
    'product_id': fields.many2one('product.product', 'Producto', required=True),
    'qty': fields.integer('Cantidad', required=True),
    'notes': fields.text('Notas', help='Motivo del Daño del Producto'),
    'state': fields.related('stock_id','state', string="Estado", type="char", size=128),
    }

    _defaults = {
    'date': datetime.now().strftime('%Y-%m-%d'),
    'qty': 1,
    }

    def on_change_sequence(self, cr, uid, ids, product_id, context=None):
        res = {}
        product_obj = self.pool.get('product.product')
        seq_id = 0
        if product_id:
            sequence = self.pool.get('ir.sequence').get(cr, uid, 'stock.rejected.lines')
            if not sequence:
                 raise osv.except_osv(
                    _('Error !'),
                    _('No se Tiene Configurado una Secuencia \n Contacte al Administrador'))
            
            res.update({'name':sequence})
        return {'value':res}

    def _check_qty(self, cr, uid, ids):
        for rec in self.browse(cr, uid, ids, context=None):
            if rec.qty>0.0:
                return True
        return False

    _constraints = [(_check_qty, 'Error: Debe ser Superior a 0', ['Cantidad'])]

stock_rejected_lines()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
