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


# Products 
class product_product(osv.osv):
    _name = 'product.product'
    _inherit ='product.product'

    _columns = {
        'sale_cost_2' : fields.float('Precio de Venta 2', digits=(14,2)),
        'sale_cost_3' : fields.float('Precio de Venta 3', digits=(14,2)),
        }

    _default = {
        }

product_product()


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
