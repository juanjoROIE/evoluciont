# Copyright 2021 Munin
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, _


class ResCompany(models.Model):
    _inherit = 'res.company'

    calendar_decline_manager_ids = fields.Many2many('res.users', string="Calendar Decline Send Notifications")

