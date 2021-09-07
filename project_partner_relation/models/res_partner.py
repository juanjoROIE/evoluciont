# Copyright 2021 Munin
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, _


class ResPartner(models.Model):
    _inherit = 'res.partner'

    partner_project_details_ids = fields.One2many(comodel_name="partner.project.details", inverse_name="partner_id",
                                                  string="Project Details", store=True)
