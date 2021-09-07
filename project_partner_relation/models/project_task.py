# Copyright 2021 Munin
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, _


class ProjectTask(models.Model):
    _inherit = 'project.task'

    project_detail_ids = fields.Many2many(comodel_name="partner.project.details",
                                          relation="x_partner_project_details_project_task_rel_3",
                                          column1="project_task_id",
                                          column2="partner_project_details_id",
                                          string="Partner Project Details",
                                          compute="get_partner_ids",
                                          readonly=False, store=False)

    @api.depends('partner_id', 'partner_id.partner_project_details_ids')
    def get_partner_ids(self):
        for record in self:
            if record.partner_id.partner_project_details_ids:
                record.project_detail_ids = record.partner_id.partner_project_details_ids.ids
            else:
                record.project_detail_ids = False
