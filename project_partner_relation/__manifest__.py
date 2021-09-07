# Copyright 2021 Munin
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Project Partner Relation',
    'description': """
        Module to add one2many related field from partner in Project""",
    'version': '14.0.1.0.0',
    'license': 'AGPL-3',
    'author': 'Munin',
    'depends': [
        'base','project'
    ],
    'data': [
        'views/res_partner.xml',
        'views/project_task.xml',
        'security/partner_project_details.xml',
    ],
    'demo': [
    ],
}
