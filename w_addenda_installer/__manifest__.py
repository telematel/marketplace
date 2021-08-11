# -*- encoding: utf-8 -*-
#
# Module written to Odoo, Open Source Management Solution
#
# Copyright (c) 2021 Telematel - http://www.telematel.com/
# All Rights Reserved.
#
# Developer(s): Nicolás Galindo
#               (ngs@tech.com)
#
########################################################################
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
########################################################################
{
    'name': 'WEDOO | Addenda Installer',
    'author': 'Wedoo ©',
    'category': 'Extra Tools',
    'sequence': 50,
    'summary': "Module to install Addendas",
    'website': 'https://wedoo.tech/',
    'version': '13.0.1.0',
    'license': 'AGPL-3',
    'description': """
Addenda Installer
=================================
This module adds an option in the account settings, to 
choose which addendas are going to be used. A many2many
field is added to choose the addendas, and based on the
user selection, the addendas will be installed. 

        """,
    'depends': [
        'base',
        'account'
    ],
    'data': [
        'views/inherit_res_config_settings.xml'
    ],
    'images': [
        'static/description/img_description.png',
        'static/description/img_screenshot.png',
    ],
    'demo': [],
    'qweb': [],
    'installable': True,
    'application': False,
}
