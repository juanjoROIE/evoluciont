# -*- coding: utf-8 -*-

# Import Odoo libs
from odoo import api, models


class GoogleService(models.TransientModel):
    _inherit = 'google.service'

    @api.model
    def _do_request(self, uri, params={}, headers={}, type='POST', preuri="https://www.googleapis.com"):
        # Initialize variables
        is_conference = self.env.context.get('is_conference')

        # If the event is a conference then add 'conferenceDataVersion' field to URI
        if is_conference:
            uri += "&conferenceDataVersion=1"

        # Call super method & return
        return super(GoogleService, self)._do_request(uri, params, headers, type, preuri)
