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

from tools.translate import _

import netsvc



class wizard_invoice_portal_cfdi(osv.osv_memory):
    _name = 'wizard.invoice.portal.cfdi'
    _description = 'Wizard para Solicitar CFDI'
    _columns = {
        'rfc': fields.char('RFC', size=32, help='Ingresa el RFC de la Empresa que solicita la Factura, si su RFC tiene el Prefijo MX eliminelo ejemplo MXKJGLFKG89 Quedaria >> KJGLFKG89', required=True),
        'sale_ref': fields.char('No. Pedido', size=64, required=True),
        'company_ids' : fields.many2many('res.company', string='Companies', readonly=True),
        }

    def _get_companies(self, cr, uid, context=None):
        user_obj = self.pool.get('res.users').browse(cr, uid, [uid], context=None)[0]
        return [user_obj.company_id.id]
    _defaults = {
        'company_ids': _get_companies,
        }
      
    def get_invoice(self, cr, uid, ids, context=None):
        ### BUSCAR EL RFC DEL CLIENTE PERO ADJUNTAR EL PREFIJO MX PARA MEXICO
        cr.execute("truncate table portal_cfdi_invoice cascade")
        admin_id = 1
        for rec in self.browse(cr, uid, ids, context=None):
            rfc = rec.rfc
            sale_ref = rec.sale_ref
            partner_obj = self.pool.get('res.partner')
            partner_id = partner_obj.search(cr, admin_id, [('vat','=','MX'+rfc)])
            
            print "###################### EL CLIENTE ES", partner_id
            if partner_id:
                partner_browse = partner_obj.browse(cr, admin_id, partner_id, context=None)[0]
                sale_obj = self.pool.get('sale.order')
                sale_order_id = sale_obj.search(cr, admin_id, [('partner_id','=',partner_id[0]),('name','=',sale_ref)])
                date_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                if sale_order_id:
                    sale_browse = sale_obj.browse(cr, admin_id, sale_order_id, context=None)[0]
                    portal_obj = self.pool.get('portal.cfdi.invoice')

                    #### FALTA LA FACTURA Y LOS DOCUMENTOS ADJUNTOS
                    attachment_list = []
                    attachment_obj = self.pool.get('ir.attachment')
                    #attachment_ids = attachment_obj.search(cr, uid, [('res_model','=','account.invoice'),('res_id','=',ids[0])], context=context)

                    invoice_obj = self.pool.get('account.invoice')
                    invoice_ids = invoice_obj.search(cr, admin_id, [('origin','=',sale_ref),('partner_id','=',partner_id[0])])
                    if invoice_ids:
                        attachment_ids = attachment_obj.search(cr, admin_id, [('res_model','=','account.invoice'),('res_id','=',invoice_ids[0])], context=context)
                        print "######################################### RECURSO ID", attachment_ids

                        for attach in attachment_obj.browse(cr, admin_id, attachment_ids, context=None):
                            attach_type = attach.name.split('.')
                            xline = (0,0,{
                                        'name': attach.datas,
                                        'type': attach_type[-1].upper() if attach_type else False,
                                        'datas_fname': attach.name,
                                        'store_fname': attach.name,
                                    })
                            attachment_list.append(xline)
                    else:
                        if sale_browse.state == 'manual':
                            sale_browse.action_invoice_create()

                            invoice_ids = invoice_obj.search(cr, admin_id, [('origin','=',sale_ref),('partner_id','=',partner_id[0])])
                            
                            
                            ### VALIDAMOS LA FACTURA
                            wf_service = netsvc.LocalService("workflow")
                            wf_service.trg_validate(admin_id, 'account.invoice', invoice_ids[0], 'invoice_open', cr)

                            
                            #######################################################################################################################
                            #######################################################################################################################
                            #######################################################################################################################
                            ########################### * FALTA ESTA PARTE DE VALIDAR EL XML                            ###########################
                            ########################### * FALTA VALIDAR LA COMPAÑIA DE LA CUAL VAMOS A CREAR LA FACTURA ###########################
                            ########################### * FALTA CAMBIAR EL NOMBRE AL DESCARGAR LOS ADJUNTOS BINARY      ###########################
                            #######################################################################################################################
                            #######################################################################################################################

                            # ************************************************* GENERAMOS EL XML *************************************************#
                            # ************************************************* ADJUNTAMOS EL XML ************************************************#
                            wizard_xml = {

                            }

                            ### ADJUNTAMOS LA FACTURA JASPER
                            invoice_id = invoice_ids[0]
                            invoice_obj.attachment_invoice_cfdi_portal(cr, admin_id, [invoice_id], invoice_id, context=None)

                            ### UNA VEZ QUE FUERON ADJUNTOS LOS BUSCAMOS                          
                            attachment_ids = attachment_obj.search(cr, admin_id, [('res_model','=','account.invoice'),('res_id','=',invoice_ids[0])], context=context)

                            for attach in attachment_obj.browse(cr, admin_id, attachment_ids, context=None):
                                attach_type = attach.name.split('.')
                                xline = (0,0,{
                                            'name': attach.datas,
                                            'type': attach_type[-1].upper() if attach_type else False,
                                            'datas_fname': attach.name,
                                            'store_fname': attach.name,
                                        })
                                attachment_list.append(xline)

                    result = {
                            'name': "Solicitud de Facturación",
                            'date': date_now,
                            'partner': partner_browse.name,
                            'sale': sale_browse.name,
                            'invoice': False,
                            'user_id': uid,
                            'line_ids': [x for x in attachment_list] if attachment_list else False,
                            }
                    portal_id = portal_obj.create(cr, uid, result)
                    return {
                            'type': 'ir.actions.act_window',
                            'name': _('Solicitud de Facturacion CFDI'),
                            'res_model': 'portal.cfdi.invoice',
                            'res_id': portal_id,
                            'view_type': 'form',
                            'view_mode': 'form',
                            'view_id': False,
                            'target': 'current',
                            'nodestroy': True,
                        }
                else:
                    raise osv.except_osv(
                                            _('Error de Captura!'),
                                            _('El Pedido %s no Existe en la Base de Datos Consulte a su Administrador') % (sale_ref))
            else:
                raise osv.except_osv(
                                    _('Error de Captura!'),
                                    _('El RFC %s no Existe en la Base de Datos Consulte a su Administrador') % (rfc))
        return True

wizard_invoice_portal_cfdi()