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
    'name': 'Portal de Auto Facturacion CFDI',
    'version': '1',
    "author" : "PonceSoft",
    "category" : "Facturacion",
    'description': """
       Este Modulo Permite tener Acceso a los Clientes a Nuestro Sistema OpenERP y ellos mismos tramitar su Factura Electronica e Imprimir Su Reporte PDF y su Archivo XML.

       Para poder Visualizar Este portal Tenemos que ir a la Parte de Configuracion y Permitir el Portal Publico.

       Tenemos que Darle permisos al Usuario anonymous para el Grupo Portal CFDI / Manager, Activamos el CheckBox.

       Listo Ahora desde Otro Navegador Ingresar al Portal Publico y Solicitar Su Factura Electronica.

       ###### REQUISITOS #######\n


       El modulo utiliza Jasper Reports Como Motor de Reportes asi que debemos tener Instalado el JDK de Java en el Servidor.

       Los Modulos de Facturacion Electronica version 7 de Vauxxo
          -l10n_mx_facturae
          -l10n_mx_facturae_cbb


       El modulo de Facturacion CFDI de HESATEC:

          - hesatec_attachment_cfdi (https://code.launchpad.net/~german-ponce/+junk/hesatec_attachment_cfdi)

       #####  A TOMAR EN CUENTA ####\n
       Para que el cliente pueda Solicitar su propia Factura y Validarla el pedido Origen dede estar en en el Estado 'Pedido a Facturar('manual')' y el metodo de Factuarion 'Bajo demanda('manual')'
      
       Instalar la Libreria QRTOOLS del Enlace:

        - https://launchpad.net/qr-tools
    """,
    "website" : "http://www.hesatecnica.com/",
    "license" : "AGPL-3",
    "depends" : ["portal","portal_crm","portal_anonymous","jasper_reports","hesatec_attachment_cfdi","l10n_mx_facturae_base","l10n_mx_facturae_cbb"],
    "init_xml" : [],
    "demo_xml" : [],
    "update_xml" : [
                    'portal_cfdi_view.xml',
                    'security/groups.xml',
                    'wizard_portal_cfdi_view.xml',
                    'security/ir.model.access.csv',
                    'account_invoice_view.xml',
                    ],
    "installable" : True,
    "active" : False,
}
