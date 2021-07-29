# Copyright 2021 Munin
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, _


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    calendar_decline_manager_ids = fields.Many2many('res.users', string="Calendar Decline Send Notifications",
                                                    related="company_id.calendar_decline_manager_ids",
                                                    readonly=False)
