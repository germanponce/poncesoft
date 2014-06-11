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
    'name': 'Registro de Productos Averiados',
    'version': '1',
    "author" : "German Ponce Dominguez",
    "category" : "stock",
    'description': """
       Adiciona la funcionalidad de describir número unidades defectuosas en los ingresos al almacén, estos son capturados en la Pestaña de Averias.
       
       - Para que funcione se necesita configurar una secuencia por defecto se crea la que tiene por Nombre Secuencia Averias se puede modificar y Adaptarse.

       - Podemos observar y Analizar cada uno de estos productos Dañados en el Menu Averias que se encuentra Ubicado Debajo de Trazabilidad en el Apartado Almacenes.
        
    """,
    "website" : "http://poncesoft.blogspot.com",
    "license" : "AGPL-3",
    "depends" : ["account","sale","stock"],
    "init_xml" : [],
    "demo_xml" : [],
    "update_xml" : [

                    #'product_view.xml',
                    'stock_rejected_view.xml',
                    'stock_view.xml',
                    'security/ir.model.access.csv',

                    ],
    "installable" : True,
    "active" : False,
}
