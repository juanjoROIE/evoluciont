# Copyright 2021 Munin
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Website Calendar Inherit',
    'description': """
        Website calendar modification to link sale order.""",
    'version': '14.0.1.0.0',
    'license': 'AGPL-3',
    'author': 'Munin',
    'depends': [
        'calendar','website_calendar','sale','sale_project'
    ],
    'data': [
        'views/calendar_event.xml',
        'views/website.xml',
    ],
    'demo': [
    ],
}
