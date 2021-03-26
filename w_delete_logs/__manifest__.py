# -*- encoding: utf-8 -*-
#
# Module written to Odoo, Open Source Management Solution
#
# Copyright (c) 2020 Wedoo - http://www.wedoo.tech/
# All Rights Reserved.
#
# Developer(s): Randy La Rosa Alvarez
#               (rra@wedoo.tech)
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
{
    'name': 'Wedoo | Delete Logs',
    'author': 'Wedoo ©',
    'category': 'Extra Tools',
    'sequence': 50,
    'summary': "Wedoo Delete Logs.",
    'website': 'https://www.wedoo.tech',
    'version': '1.0',
    'license': 'AGPL-3',
    'description': """
Wedoo | Delete Logs
===================================================
This module delete any model logs and to program 
the elimination times.

        """,
    'depends': [
        'base', 'mail'
    ],
    'data': [
        'data/cron.xml',
        'views/inherit_res_config_settings.xml'

    ],
     'images': [
        'static/description/log_description.jpg',
        'static/description/log_screenshot.jpg',
    ],
    'demo': [],
    'qweb': [],
    'application': False,
    'installable': True,
}


