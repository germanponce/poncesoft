# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2013 HESATEC (<http://www.hesatecnica.com>).
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

from openerp import tools

from openerp.osv import fields, osv, orm

from datetime import time, datetime

import hashlib
import itertools
import logging
import os
import re

from openerp import tools
from openerp import SUPERUSER_ID

_logger = logging.getLogger(__name__)

class portal_cfdi_invoice(osv.osv):
    _name = 'portal.cfdi.invoice'
    _description = 'Formulario Resultado de la Facturacion'
    _columns = {
        'name': fields.char('Referencia', size=64),
        'date': fields.datetime('Fecha Solicitud'),
        'partner': fields.char('Cliente', size=64),
        'sale': fields.char('Pedido', size=64),
        'invoice': fields.char('Factura', size=64),
        'user_id': fields.many2one('res.users','Usuario Peticion'),
        'line_ids': fields.one2many('portal.cfdi.invoice.line', 'line_id','Documentos Adjuntos', ondelete="cascade"),
    }

portal_cfdi_invoice()


class portal_cfdi_invoice_line(osv.osv):
    _name = 'portal.cfdi.invoice.line'
    _description = 'Documentos Adjuntos'
    _columns = {
        'datas_fname': fields.char('File Name',size=256, ondelete="cascade"),
        'name': fields.binary('Documento Adjunto', ondelete="cascade"),
        'type': fields.char('Tipo Archivo', size=64, ondelete="cascade"),
        'line_id': fields.many2one('portal.cfdi.invoice','ID Referencia', ondelete="cascade"),
        'store_fname': fields.char('Stored Filename', size=256, ondelete="cascade"),
    }

portal_cfdi_invoice_line()