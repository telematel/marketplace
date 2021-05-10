# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ProjectTask(models.Model):
    _inherit = 'project.task'

    out_of_stage = fields.Boolean(
        compute='_compute_parent_stage', help='Has the same state of parent task')
    parent_progress_checklist = fields.Float(
        related='parent_id.progress_checklist', readonly=True)
    stage_color = fields.Char(
        compute='_set_stage_style')

    @api.depends('stage_id', 'parent_id.stage_id')
    def _compute_parent_stage(self):
        for record in self:
            record.out_of_stage = record.parent_id.stage_id.id != record.stage_id.id

    @api.depends('stage_id.color')
    def _set_stage_style(self):
        for record in self:
            if record.stage_id.color:
                record.stage_color = 'background-color: {};'.format(record.stage_id.color)
            else:
                record.stage_color = ''
