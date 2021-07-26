# -*- encoding: utf-8 -*-
#
# Module written to Odoo, Open Source Management Solution
#
# Copyright (c) 2021 Wedoo - http://www.wedoo.tech
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
#
########################################################################
{
    'name': "Wedoo | Widget Open Many2many Tags",
    'author': 'Wedoo ©',
    'category': 'Extra Tools',
    'sequence': 50,
    'summary': """
        It allows to open the form in the many2many_tags when 
        clicking.
    """,
    'website': 'https://www.wedoo.tech',
    'version': '13.0.1.0',
    'license': 'AGPL-3',
    'description': """
Wedoo | Widget Open Many2many Tags
----------------------------------
This widget works similar to many2many_tags, but with the 
difference that clicking on an element opens the corresponding form.
    """,
    'depends': ['base'],
    'data': [
        'views/assets.xml'
    ],
    'demo': [],
    'images': [
        'static/description/img_description.png',
        'static/description/img_screenshot.png',
    ],
    'installable': True,
    'application': False,
}
