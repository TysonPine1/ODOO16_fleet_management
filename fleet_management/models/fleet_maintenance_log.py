from odoo import models, fields, api
from datetime import date

class FleetMaintenanceLog(models.Model):
    _name = 'fleet.maintenance.log'
    _description = 'Fleet Maintenance Log'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    vehicle_id = fields.Many2one('fleet.management', string="Vehicle", required=True)
    maintenance_type = fields.Selection([
        ('oil_change', 'Oil Change'),
        ('tire_change', 'Tire Change'),
        ('brake_inspection', 'Brake Inspection'),
        ('engine_tuneup', 'Engine Tune-Up')
    ], string="Maintenance Type", required=True)
    maintenance_cost = fields.Float(string="Maintenance Cost", required=True)
    date = fields.Date(string="Date", required=True)
    next_due_date = fields.Date(string="Next Due Date")
    notes = fields.Text(string="Notes")
    state = fields.Selection([
        ('scheduled', 'Scheduled'),
        ('completed', 'Completed'),
        ('canceled', 'Canceled')
    ], string="Status", default='scheduled')
    maintenance_due = fields.Boolean(string="Due for Maintenance", compute='_compute_maintenance_due', store=True)

    def _cron_check_maintenance_due(self):
        today = fields.Date.today()
        logs = self.search([
            # ('next_due_date', '!=', False),
            ('next_due_date', '<=', today),
            ('state', '=', 'scheduled')
        ])

        admin_partners = self.env['res.users'].browse(1).mapped('partner_id')

        for rec in logs:
            partners_to_notify = admin_partners 
            if rec.vehicle_id.driver_name:
                partners_to_notify |= rec.vehicle_id.driver_name
            
            rec.message_subscribe(partner_ids=partners_to_notify.ids) 

            rec.message_post(
                body=f"Maintenance is due for vehicle {rec.vehicle_id.name} on {rec.next_due_date}.",
                subject="Maintenance Due Reminder",
                message_type="comment",         
                subtype_xmlid="mail.mt_comment" 
            )

    @api.depends('next_due_date', 'state')
    def _compute_maintenance_due(self):
        today = date.today()
        for rec in self:
            rec.maintenance_due = bool(
                rec.next_due_date and rec.next_due_date <= today and rec.state == 'scheduled'
            )