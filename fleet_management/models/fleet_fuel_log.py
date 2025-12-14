from odoo import models, fields
from odoo.addons.l10n_din5008_purchase.models import purchase

class FleetFuelLog(models.Model):
    _name = 'fleet.fuel.log'
    _description = 'Fleet Fuel Log'

    vehicle_id = fields.Many2one('fleet.management', string='Vehicle', required=True)
    date = fields.Date(string='Date', required=True)
    fuel_type = fields.Selection([('petrol', 'Petrol'), ('diesel', 'Diesel'), ('electric', 'Electric'), ('hybrid', 'Hybrid')], string='Fuel Type', required=True)
    liters = fields.Float(string='Liters', required=True)
    fuel_cost = fields.Float(string='Cost', required=True)
    odometer = fields.Float(string='Odometer Reading (km)', required=True)
    notes = fields.Text(string='Notes')