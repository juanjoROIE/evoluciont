# Copyright 2021 Munin
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, _


class PartnerProjectDetails(models.Model):
    _name = 'partner.project.details'
    _description = 'Partner Project Details'  # TODO

    name = fields.Text(string="Description")
    date = fields.Date(default=fields.Date.context_today)
    partner_id = fields.Many2one('res.partner', string="Related Partner", copy=False)
    project_id = fields.Many2one('project.task', string="Related Project", copy=False)
    origin = fields.Char('origin', copy=False)
