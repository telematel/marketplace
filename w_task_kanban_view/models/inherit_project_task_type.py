# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ProjectTaskType(models.Model):
    _inherit = 'project.task.type'

    color = fields.Char(
        string='Color Index')
