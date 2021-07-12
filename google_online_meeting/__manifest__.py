# -*- coding: utf-8 -*-

{
    "name": "Google Meeting",
    "author": "TuOdoo",
    "category": "Tools",
    "description": """Create meets from calendar.
    """,
    "support": "odoo@alpha-brains.com",
    "website": "https://www.tuodoo.com",
    "version": "1.0.0",
    "depends": [
        'google_calendar'
    ],
    "data": [
        'views/calendar_event_views.xml',
    ],
    "images": [
    ],
    "application": False,
    "installable": True,
}
