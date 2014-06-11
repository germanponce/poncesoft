# -*- encoding: utf-8 -*-
###########################################################################
#    Module Writen to OpenERP, Open Source Management Solution
#
#    Copyright (c) 2010 moylop260 - http://www.hesatecnica.com.com/
#    All Rights Reserved.
#    info skype: german_442 email: (german.ponce@hesatecnica.com)
############################################################################
#    Coded by: german_442 email: (german.ponce@hesatecnica.com)
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
import tempfile
from xml.dom import minidom
import os
import base64
import hashlib
import tempfile
import os
import codecs


class account_invoice(osv.osv):
    _inherit ='account.invoice'
    _columns = {
    }

    def attachment_invoice_cfdi_portal(self, cr, uid, ids, active_id, context=None):
        ## DEBE RECIBIR UN ACTIVE ID DEL REGISTRO DONDE ADJUNTARA LA FACTURA
        #### --- DICCCIONARIO VALUE EN DONDE CREAMOS UN ACTION REPORT EN EN EL MODELO TYPE --- ######
        value = {
            'type': 'ir.actions.report.xml', #### INDICAMOS QUE EL RETORNO ES DEL MODELO ir.actions.report.xml
            'report_name': 'account_invoice_portal_cfdi_report', #### NOMBRE DEL REPORTE CON EL QUE LO GUARDAMOS EN LA CARPETA REPORT SIN LA EXTENSION .jrxml EN MI CASO SE LLAMA Factura-2013-Final.jrxml ES IMPORTANTE QUE SE ENCUENTRE DENTRO DE LA CARPETA REPORT DEL MODULO
            'datas': {
                        'model' : 'account.invoice', #### MODELO DEL CUAL OBTENDRA LA INFORMACION EL REPORTE
                        'ids'   : [active_id], ### INDICAMOS LOS IDS DE LOS CUALES TOMARA LA INFORMACION EL REPORTE
                        }
                    }

        #### --- CONSTRUIMOS EL NOMBRE PARA EL REPORTE --- ####
        file_name = ""
        report_name = value['report_name']

        account_obj = self.pool.get('account.invoice')
        for rec in account_obj.browse(cr, uid, [active_id], context=context):
            vat = rec.company_emitter_id.address_invoice_parent_company_id.vat.replace('MX','')
            serie = rec.journal_id.sequence_id.approval_id.serie
            if vat:
                file_name = vat + '_' + serie + '_' +str(rec.number)
            else:
                file_name = "Factura CFDI "+str(rec.number)

        #### --- BUSCAMOS QUE EL REGISTRO DE LA FACTURA NO TENGA ADJUNTO UN ARCHIVO PDF PREVIAMENTE CARGADO CON ESTA FUNCION --- ####
        attachment_ids = self.pool.get('ir.attachment').search(cr, uid, [("name","=",file_name+'.pdf')], limit=1, context=context)

        #### --- EN CASO DE QUE NO TENGA UN ARCHIVO ADJUNTO ENTONCES PROCEDEMOS A CREARLO PARA ELLO HACEMOS USO DE LA FUNCION CREATE_REPORT_JASPER --- ####
        if not attachment_ids:
            if not context:
                context = {}
            id = ids[0]
            (fileno, fname) = tempfile.mkstemp(
                '.pdf', 'openerp_' + (False or '') + '__facturae__')
            os.close(fileno)
            file = self.create_report_jasper_portal(cr, uid, [active_id], 'account_invoice_portal_cfdi_report', file_name) ### USAMOS LA FUNCION CREATE_REPORT_JASPER Y LOS PARAMETROS A RECIBIR SON IDS A DONDE CREARA EL ADJUNTO,EL NOMBRE DEL REPORTE RML O JASPER Y EL NOMBRE PARA CREAR EL REPORTE
            is_file = file[0]
            fname = file[1]
            if is_file and os.path.isfile(fname):
                f = open(fname, "r")
                data = f.read()
                f.close()
                # datas = data and base64.encodestring(data)
                # print "##################################################### DATASSSSS", datas
                data_attach = {
                    'name': file_name+'.pdf',
                    'datas_fname': file_name+'.pdf',
                    'description': 'account_invoice_portal_cfdi_report PDF',
                    'res_model': 'account.invoice',
                    'res_id': active_id,
                    'type': 'binary',
                    'datas': data and base64.encodestring(data) or None,
                    'store_fname': file_name+'.pdf',
                }
                self.pool.get('ir.attachment').create( cr, uid, data_attach, context=context)

        return value

    def create_report_jasper_portal(self, cr, uid, res_ids, report_name=False, file_name=False):
        #### --- ESTA FUNCION CREA Y PROCESA EL REPORTE PARA PODER TENERLO EN MEMORIA TEMPORALMENTE --- ####
        if not report_name or not res_ids:
            return (False, Exception('Report name and Resources ids are required !!!'))
        ret_file_name = '/tmp/'+file_name+'.pdf' #### NOMBRE TEMPORAL DEL REPORTE
        service = netsvc.LocalService("report."+report_name) #### EJECUTAMOS NETSVC PARA EJECUAL PROCESOS LOCALES DE OPENERP EN ESTE CASO SIMULAMOS LA IMPRESION DEL REPORTE
        (result, format) = service.create(cr, uid, res_ids, {'model' : 'account.invoice'}, {})
        fp = open(ret_file_name, 'wb+');
        fp.write(result);
        fp.close();
        return (True, ret_file_name)   
    
account_invoice()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
