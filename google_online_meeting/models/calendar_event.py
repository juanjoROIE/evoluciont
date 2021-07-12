# -*- coding: utf-8 -*-
# Import Python libs
import random
import string
import logging

# Import Odoo libs
from odoo import _, api, fields, models

# Global variables
_logger = logging.getLogger(__name__)


class ABTCalendarEvent(models.Model):
    _inherit = "calendar.event"

    google_solution = fields.Selection([
        ('none', 'None'),
        ('eventHangout', 'Hangouts'),
        ('hangoutsMeet', 'Google Meet'),
    ],
        string='Online meeting solution',
        default='none'
    )
    google_meet_conference_code = fields.Char(
        'Google Meet Code',
        readonly=True,
        store=True,
        copy=False,
        help='This code is used to join the online meeting on Google meet (meet.google.com).'
    )
    google_conference_signature = fields.Char(
        'Google Conference Signature',
        readonly=True,
        store=True,
        copy=False,
        help='This signature is the identifier of the conference on Google services.'
    )
    google_conference_uri = fields.Char(
        'Google Conference URI',
        readonly=True,
        store=True,
        copy=False,
        help='This URI is used to join the meeting.'
    )
    google_conference_entry_point_type = fields.Char(
        'Entry Point Type',
        readonly=True,
        store=True,
        copy=False,
        help='This is the entry type of the meeting.'
    )
    conference_requestId = fields.Char(
        'Conference Request ID',
        readonly=True,
        store=True,
        copy=False,
        help='Technical field used to send the request to Google Calendar. This field should be not visible to users'
    )

    @api.model
    def _generate_random_unique_conference_request_id(self, event_id):
        """ Get a random token (32 characters mixed with uppercase, lowercase and digits)"""
        # Initialize variables
        new_token = ''
        request_pattern = 'odoo{id}-{token}-abt'

        # Iterate for random characters to generate random token
        for i in range(23 - len(str(event_id))):
            new_token += random.choice(string.ascii_uppercase + string.digits + string.ascii_lowercase)

        # Build the request id according to the above defined pattern
        request_id = request_pattern.format(id=event_id, token=new_token)

        # Return
        return request_id

    def _generate_conference_request_id(self):
        """
        If the event has no Google Conference ID generate an ID add save it on conference_requestId field
        """
        self.ensure_one()

        # If no ID is defined for this event then create a new one
        if not self.conference_requestId:
            # Generate random & unique Conference ID
            request_id = self._generate_random_unique_conference_request_id(self.id)

            # Save the Conference Request ID on conference_requestId field
            self.write({
                'conference_requestId': request_id
            })

            # Log the event for debugging purpose
            _logger.debug(
                _('Generate Google Conference Request ID for the event %s: %s.') % (self.name, request_id)
            )

        # Return the Conference Request ID
        return self.conference_requestId

    def is_google_conference(self):
        """
        Determine if the current event is a google conference event
        :return: True is the event is a google conference. False if not.
        """
        self.ensure_one()
        return self.google_solution not in ('none', False)

    def _update_event_conference_data(self, conference_data):
        """
        Update the current event with the conference data.
        :param conference_data: Dict contains the conference data returned from Google Calendar
        """
        # If no conference data is provided by Google calendar then do nothing
        if conference_data:
            # Get the entry point data
            entry_point = conference_data.get('entryPoints', [{}])[0]

            # Update the event with the conference data
            self.write({
                'google_meet_conference_code': conference_data.get('conferenceId'),
                'google_conference_signature': conference_data.get('signature'),
                'google_conference_uri': entry_point.get('uri'),
                'google_conference_entry_point_type': entry_point.get('entryPointType'),
                'google_solution': conference_data.get('conferenceSolution', {}).get('key', {}).get('type',
                                                                                                        'none'),
            })
