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

    def print_invoice_ticket(self, cr, uid, ids, context=None):
        value = {
            'type': 'ir.actions.report.xml',
            'report_name': 'Factura_Ticket',
            'datas': {
                        'model' : 'account.invoice',
                        'ids'   : ids,
                        }
                    }

        return value

account_invoice()