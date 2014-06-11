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
    'name': 'Autorización de Mercancia',
    'version': '1',
    "author" : "German Ponce Dominguez",
    "category" : "stock",
    'description': """

        Adiciona la Funcionalidad de los Albaranes de Salida para añadir un reporte de Expedicion y Autorización de la Misma en un Boton Llamado Autorización de Mercancia.
        
            - Necesitamos Tener Instalado en nuestro Servidor el JDK de Oracle o el OpenJDK version 7 o 6
                sudo apt-get install openjdk-7-jdk
            - Necesitamos Tener Instalado en la base de OpenERP el modulo jasper_reports.
                
    """,
    "website" : "http://poncesoft.blogspot.com",
    "license" : "AGPL-3",
    "depends" : ["account","sale","stock","jasper_reports"],
    "init_xml" : [],
    "demo_xml" : [],
    "update_xml" : [
                    'stock_receipt_view.xml',
                    'stock_view.xml',
                    #'security/ir.model.access.csv',
                    ],
    "installable" : True,
    "active" : False,
}
