# -*- coding: utf-8 -*-
# Part of Alpha Brains Technologies.
# Import Python libs
import logging

# Import Odoo libs
from odoo import _, models
from odoo.addons.google_calendar.models.google_calendar import GoogleCalendar, status_response

# Global variables
_logger = logging.getLogger(__name__)


class ABTGoogleCalendar(models.AbstractModel):
    _inherit = 'google.%s' % GoogleCalendar.STR_SERVICE

    def generate_data(self, event, isCreating=False):
        # Call super method to get the default generated data
        data = super(ABTGoogleCalendar, self).generate_data(event, isCreating)

        # If the user choose one of Google Online Meeting solutions then add the necessary data to create
        # the online meeting event on Google Calendar
        if event.is_google_conference():
            # Generate the Request ID
            request_id = event._generate_conference_request_id()

            # Create the conference data
            conference_data = {
                'createRequest': {
                    'requestId': request_id,
                    'conferenceSolutionKey': {
                        'type': event.abt_google_solution
                    }
                }
            }

            # Add the conference data to the returned data
            data['conferenceData'] = conference_data

        # Return
        return data

    def create_an_event(self, event):
        """
        Override this method to update the event with the conference  data
        """
        # Initialize variables
        event_is_conference = event.is_google_conference()

        # Build the context
        context = dict(self.env.context, abt_is_conference=event_is_conference)

        # Call super method to get response from Google Services
        status, response, ask_time = super(ABTGoogleCalendar, self.with_context(context)).create_an_event(event)

        # If the status code is 'SUCCESS' and the event is an Google Conference then update the event
        # with the conference data
        if status_response(status) and event_is_conference:
            # Get the Conference Data
            conference_data = response.get('conferenceData')

            # Log the conference data for debugging purpose
            _logger.debug(
                _('Conference Data returned from Google Services: %s') % str(conference_data)
            )

            # Update the event with the conference data
            event._update_event_conference_data(conference_data)

        # return
        return status, response, ask_time

    def update_from_google(self, event, single_event_dict, type):
        # Call super method
        res = super(ABTGoogleCalendar, self).update_from_google(event, single_event_dict, type)

        # Initialize variables
        CalendarEvent = self.env['calendar.event']

        # If new event is created on Odoo
        if type == "create":
            # Browse the Event by ID
            event_id = CalendarEvent.browse(res)

            # Get the conference data
            conference_data = single_event_dict.get('conferenceData')

            # Log the conference data for debugging purpose
            _logger.debug(
                _('Conference Data returned from Google Services: %s') % str(conference_data)
            )

            # Update the event with the conference data
            event_id._update_event_conference_data(conference_data)

        # Return
        return res
