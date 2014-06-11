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
    'name': 'Dominio de Productos por Categoria',
    'version': '1',
    "author" : "German Ponce Dominguez",
    "category" : "stock",
    'description': """
       - Adiciona la funcionalidad para el pedido de venta filtrando los productos por Categoria.
       - Adiciona la funcionalidad para el pedido de venta del TPV filtrando los productos por Categoria.
       - Agrega 2 Campos extra para Precio de Venta, estos campos Nos serviran para poder Crear Tarifas basados en Estos campos para cada cliente.
            * Para Poder Crear una Tarifa de Venta que Utilice estos campos primero debemos crear un Tipo de Precio en el apartado Ventas --> Configuracion --> Tarifas --> Tipos de Precio, aqui creamos un Tipo de Precio que utilice alguno de los campos anteriormente creados Precio de Venta 2 o Precio de Venta 3.
            * Una ves creado el Tipo de Precio basado en estos campos, Creamos una Tarifa en Ventas --> Configuracion --> Tarifas --> Tarifas, creamos una Tarifa le ponemos como Nombre Tarifa de Venta 2 si utilizamos el Precio 2 de Venta.
            * Le creamos uan version de Tarifa le ponemos por Nombre por Defecto, le agregamos una secuencia o regla y esta la Basamos en el apartado Calculo de Precio, seleccionamos Precio de Venta 2.
            * Repetimos los Pasos para crear Una tarifa Precio de Venta 3.
            * Listo Ahora asignamos estas tarifas a Cada cliente y nos permiten que al realizar un pedido de Venta estemos Utilizando los Precios Definidos en estos Campos.
    """,
    "website" : "http://poncesoft.blogspot.com",
    "license" : "AGPL-3",
    "depends" : ["sale","product","point_of_sale"],
    "init_xml" : [],
    "demo_xml" : [],
    "update_xml" : [
                    'product_view.xml',
                    'sale_view.xml',
                    'pos_view.xml',

                    ],
    "installable" : True,
    "active" : False,
}
