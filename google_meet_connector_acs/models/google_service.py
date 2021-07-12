# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _

TIMEOUT = 20


class GoogleService(models.AbstractModel):
    _inherit = 'google.service'

    @api.model
    def _do_request(self, uri, params=None, headers=None, method='POST', preuri="https://www.googleapis.com", timeout=TIMEOUT):
        split_vals = uri.split('/')
        if split_vals and 'calendars' in split_vals and 'events' in split_vals:
            uri = uri + '?conferenceDataVersion=1&sendNotifications=True'
        res = super(GoogleService, self)._do_request(uri=uri, params=params, headers=headers, method=method, preuri=preuri, timeout=timeout)
        return res
