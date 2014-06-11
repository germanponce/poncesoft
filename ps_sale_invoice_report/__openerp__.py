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
    'name': 'Reporte de Identificacion de Pedidos(Facturacion)',
    'version': '1',
    "author" : "German Ponce Dominguez",
    "category" : "account",
    'description': """

            Este modulo permite que al crear una Factura desde los pedidos de Venta se tenga la referencia en el Reporte de cada uno de Ellos.

            Instrucciones:
                - 1. Para poder Utilizar el Modulo necesitamos tener Instalado: Modulo Jasper Reports y el Servidor de OpenERP tenga el JDK de Java.
                - 2. Instalar este modulo.
                - 3. Crear una Factura tomando Varios pedidos de Venta con el Asistente de Realizar Facturas al seleccionar Registros de Ventas y al crear la Factura Agrupar por Cliente.
            Para poder Visualizar el Reporte Pulsar el Boton Factura Detallada y este Descargara el Reporte.     
    """,
    "website" : "http://poncesoft.blogspot.com",
    "license" : "AGPL-3",
    "depends" : ["account","sale","jasper_reports"],
    "init_xml" : [],
    "demo_xml" : [],
    "update_xml" : [
                    'account_view.xml',
                    'security/ir.model.access.csv',
                    ],
    "installable" : True,
    "active" : False,
}
