# Copyright 2021 Munin
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, _
from odoo.tools.safe_eval import safe_eval
from odoo.exceptions import UserError


class CalendarEvent(models.Model):
    _inherit = 'calendar.event'

    sale_id = fields.Many2one(comodel_name="sale.order", string="Sale Order", required=False, copy=False)
    sale_tasks_count = fields.Integer(string='Tasks', compute='_compute_tasks_ids', groups="project.group_project_user")

    def create_sale_order(self):
        user = self.user_id.partner_id.ids
        partner = self.partner_ids.filtered(lambda x: x.id not in user) if \
            self.partner_ids else False
        if not partner:
            raise UserError("Agregar un Usuario como Participante")
        partner = partner[0]
        sale = self.env['sale.order'].create({
            'partner_id': partner.id,
            'partner_invoice_id': partner.id,
            'partner_shipping_id': partner.id,
        })
        if not sale:
            return False
        sale.onchange_partner_id()
        view = self.env.ref('sale.view_order_form')
        self.sale_id = sale.id
        context = dict(self._context)
        context['form_view_initial_mode'] = 'edit'
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'sale.order',
            'view_type': 'form',
            'view_mode': 'form',
            'views': [(view.id, 'form')],
            'target': 'current',
            'res_id': sale.id,
            'context': context}

    @api.depends('sale_id.tasks_ids')
    def _compute_tasks_ids(self):
        for order in self:
            order.sale_tasks_count = len(order.sale_id.tasks_ids)

    def action_view_task_sale(self):
        self.ensure_one()

        list_view_id = self.env.ref('project.view_task_tree2').id
        form_view_id = self.env.ref('project.view_task_form2').id

        action = {'type': 'ir.actions.act_window_close'}
        task_projects = self.sale_id.tasks_ids.mapped('project_id')
        if len(task_projects) == 1 and len(self.sale_id.tasks_ids) > 1:  # redirect to task of the project (with kanban
            # stage, ...)
            action = self.with_context(active_id=task_projects.id).env['ir.actions.actions']._for_xml_id(
                'project.act_project_project_2_project_task_all')
            action['domain'] = [('id', 'in', self.sale_id.tasks_ids.ids)]
            if action.get('context'):
                eval_context = self.env['ir.actions.actions']._get_eval_context()
                eval_context.update({'active_id': task_projects.id})
                action_context = safe_eval(action['context'], eval_context)
                action_context.update(eval_context)
                action['context'] = action_context
        else:
            action = self.env["ir.actions.actions"]._for_xml_id("project.action_view_task")
            action['context'] = {}  # erase default context to avoid default filter
            if len(self.sale_id.tasks_ids) > 1:  # cross project kanban task
                action['views'] = [[False, 'kanban'], [list_view_id, 'tree'],
                                   [form_view_id, 'form'], [False, 'graph'],
                                   [False, 'calendar'], [False, 'pivot']]
            elif len(self.sale_id.tasks_ids) == 1:  # single task -> form view
                action['views'] = [(form_view_id, 'form')]
                action['res_id'] = self.sale_id.tasks_ids.id
        # filter on the task of the current SO
        action.setdefault('context', {})
        action['context'].update({'search_default_sale_order_id': self.sale_id.id})
        return action
