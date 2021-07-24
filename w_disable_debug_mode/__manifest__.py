# -*- encoding: utf-8 -*-
#
# Module written to Odoo, Open Source Management Solution
#
# Copyright (c) 2019 Wedoo - http://www.wedoo.tech/
# All Rights Reserved.
#
# Developer(s): Randy La Rosa Alvarez
#               (randi.larosa@telematel.com)
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
    'name': 'Wedoo | Disable Debug Mode',
    'author': 'Wedoo ©',
    'category': 'Extra Tools',
    'sequence': 50,
    'summary': "This module disables debug mode for users who do not have the "
               "'Enable debug mode' permission.",
    'website': 'https://www.wedoo.tech',
    'version': '13.0.1.0',
    'license': 'AGPL-3',
    'depends': [
        'web'
    ],
    'data': [
        'security/w_disable_debug_mode_security.xml'
    ],
    'demo': [],
    'qweb': [],
    'images': [
        'static/description/img_description.png',
        'static/description/img_screenshot.png',
    ],
    'installable': True,
    'application': False,
}
