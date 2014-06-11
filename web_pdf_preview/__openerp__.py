# -*- coding: utf-8 -*-
##############################################################################
#    Web PDF Report Preview & Print
#    Copyright 2012 wangbuke <wangbuke@gmail.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    Modificado por German Ponce
#    german.ponce@hesatecnica.com
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
    "name": "Web PDF Report Preview & Print",
    'version': '1.0',
    'category': 'Web',
    'description': """Web PDF Report Preview & Print

        Preview & Print PDF report in your browser.

        * For IE, Adobe Reader is required.
        * For Chrome , nothing is requried.
        * For Firefox, Adobe Reader is required.

        Este modulo permite a los Usuarios de OpenERP tener un Preview del Documento que van a Imprimir.
        Para Evitar la tarea de Tener que Descargar los Documentos y Abrirlos con Nuestro Visualizador de Archivos PDF, si no utilizar el predeterminado por los Navegadores.

        Para que La Impresión se Vaya Directo a Una Impresora:

            - Configurar la Impresora en la Maquina y ponerla como Predeterminada.
            - Iniciamos el Chrome como Kiosk:
                - Ubuntu --> Desde una Terminal google-chrome --kiosk --kiosk-printing (Agregamos la url de Open, No es Obligatoria).
                - Windows --> Agregamos al Acceso Directo de Chrome  --kiosk --kiosk-printing.
            - Al darle Imprimir en Automatico se Imprime Directo a Esa Impresora.
        Nota:
            Es Importante que no se tenga deshabilitado el PDF Preview en Chrome.

    """,
    'author': 'german.ponce@hesatecnica.com',
    'website': 'http://buke.github.io, http://poncesoft.blogspot.com',
    'license': 'AGPL-3',
    'depends': ['web'],
    'data': [],
    'auto_install': False,
    'web_preload': True,
    'js': ['static/src/js/web_pdf_preview.js'],
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
