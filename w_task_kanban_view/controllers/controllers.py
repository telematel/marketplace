# -*- coding: utf-8 -*-
from odoo import http

# class WTaskKanbanView(http.Controller):
#     @http.route('/w_task_kanban_view/w_task_kanban_view/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/w_task_kanban_view/w_task_kanban_view/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('w_task_kanban_view.listing', {
#             'root': '/w_task_kanban_view/w_task_kanban_view',
#             'objects': http.request.env['w_task_kanban_view.w_task_kanban_view'].search([]),
#         })

#     @http.route('/w_task_kanban_view/w_task_kanban_view/objects/<model("w_task_kanban_view.w_task_kanban_view"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('w_task_kanban_view.object', {
#             'object': obj
#         })