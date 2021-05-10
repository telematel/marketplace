# -*- coding: utf-8 -*-
{
    'name': "WEDOO | Task Kanban View",
    'author': 'Wedoo ©',
    'category': 'Tools',
    'sequence': 50,
    'summary': "Parent task on Kanban View",
    'website': 'https://www.wedoo.tech',
    'version': '13.0.0.0',
    'license': 'LGPL-3',
    'description': """
        Task Kanban View
        =================
        This module allows you to display the main task if it is associated with any task in the project's kanban view.
    """,
    'depends': ['project', 'web_widget_colorpicker'],

    'data': [
        'views/inherit_project_view.xml',
        'views/inherit_project_type_view.xml',
        'views/assets.xml',
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
