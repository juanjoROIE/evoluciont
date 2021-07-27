# Copyright 2021 Munin
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, _
import time


# class Meeting(models.Model):
#     _name = 'calendar.event'
#     _inherit = ['calendar.event', 'mail.activity.mixin']  # add the activity mixin. UPDATE: IT DOESNT WORK.


class CalendarAttendee(models.Model):
    _inherit = 'calendar.attendee'

    def do_decline(self):
        res = super(CalendarAttendee, self).do_decline()
        for attendee in self:
            manager_partner = attendee.event_id.user_id.partner_id.ids
            body = _("<b>%s: %s</b> has declined invitation.<br/>date: %s") % (attendee.event_id.name,
                                                                               attendee.common_name,
                                                                               fields.Date.context_today(self))
            self.env['mail.message'].sudo().create({
                'author_id': attendee.event_id.user_id.partner_id.id,
                'date': time.strftime('%Y-%m-%d %H:%M:%S'),
                'message_type': 'comment',
                'record_name': attendee.event_id.name,
                'model': 'calendar.event',
                'res_id': attendee.event_id.id,
                'partner_ids': [(6, 0, manager_partner)],
                'notification_ids': [(0, 0, {
                    'notification_type': 'email',
                    'res_partner_id': partner,
                }) for partner in manager_partner],
                'subject': body,
                'body': body,
            })
            send_mail = self.env['mail.mail'].sudo().create({
                'subject': _('Calendar event: %s , declined.') % attendee.event_id.name,
                'author_id': self.env.user.partner_id.id,
                'body_html': body,
                'recipient_ids': [(6, 0, manager_partner)],
            })
            send_mail.sudo().send()
        return res
