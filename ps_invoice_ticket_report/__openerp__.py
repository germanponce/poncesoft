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
    'name': 'Reporte Factura Ticket',
    'version': '1',
    "author" : "German Ponce Dominguez",
    "category" : "account",
    'description': """

            Este modulo permite Imprimir una Factura en Tamaño Ticket, especial para el Punto de Venta.
            Para Funcionar:
                - El modulo jasper_reports
                - El JDK de Java en el Servidor.
                - Modulo Facturacion OpenERP.   
    """,
    "website" : "http://poncesoft.blogspot.com",
    "license" : "AGPL-3",
    "depends" : ["account","sale","jasper_reports"],
    "init_xml" : [],
    "demo_xml" : [],
    "update_xml" : [
                    'account_view.xml',
                    ],
    "installable" : True,
    "active" : False,
}
