from odoo import models, fields, api
import logging
_logger = logging.getLogger(__name__)

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


    def _cron_check_maintenance_due(self):
        today = fields.Date.today()
        logs = self.search([
            ('next_due_date', '!=', False),
            ('next_due_date', '<=', today),
            ('state', '=', 'scheduled')
        ])
        
        for rec in logs:
            rec.message_post(
                body=f"Maintenance is due for vehicle {rec.vehicle_id.name} on {rec.next_due_date}.",
                subject="Maintenance Due Reminder",
                message_type="notification",       
                subtype_xmlid="mail.mt_comment",  
        )