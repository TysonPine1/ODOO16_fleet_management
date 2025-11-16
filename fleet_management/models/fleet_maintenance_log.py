from odoo import models, fields, api

class FleetMaintenanceLog(models.Model):
    _name = 'fleet.maintenance.log'
    _description = 'Fleet Maintenance Log'

    vehicle_id = fields.Many2one('fleet.management', string="Vehicle", required=True)
    maintenance_type = fields.Selection([
        ('oil_change', 'Oil Change'),
        ('tire_change', 'Tire Change'),
        ('brake_inspection', 'Brake Inspection'),
        ('engine_tuneup', 'Engine Tune-Up')
    ], string="Maintenance Type", required=True)
    cost = fields.Float(string="Cost", required=True)
    date = fields.Date(string="Date", required=True)
    next_due_date = fields.Date(string="Next Due Date")
    notes = fields.Text(string="Notes")
    state = fields.Selection([
        ('scheduled', 'Scheduled'),
        ('completed', 'Completed'),
        ('canceled', 'Canceled')
    ], string="Status", default='scheduled')
