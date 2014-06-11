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
{
    'name': 'Facturacion sin Existencias',
    'version': '1',
    "author" : "German Ponce Dominguez",
    "category" : "Ventas",
    'description': """

            - Este modulo no Permite Confimar una Venta si no Se tiene Stock de alguno de los Productos A menos que se Autorice la Venta.
            
            - Este modulo no Permite Facturar una Venta si no Se tiene Stock de alguno de los Productos A menos que se Autorice la Facturacion.
            
            - Para ello existe un Boton llamo Autorizar Venta, pide la contraseña del Usuario que debe tener Permisos especiales.
            
            - Existe un Grupo Llamado Facturacion Especial y es el que permite a los usuarios de ese Grupo, autorizar Facturas sin Stock.    
    """,
    "website" : "http://poncesoft.blogspot.com",
    "license" : "AGPL-3",
    "depends" : ["account","sale","jasper_reports"],
    "init_xml" : [],
    "demo_xml" : [],
    "update_xml" : [
                    'sale_view.xml',
                    'security/ir.model.access.csv',
                    ],
    "installable" : True,
    "active" : False,
}
