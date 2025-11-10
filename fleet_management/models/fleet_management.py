from odoo import models, fields

class FleetVehicle(models.Model):
    _name = "fleet.management"

    name = fields.Char(string="Vehicle Name", required=True)
    license_plate = fields.Char(string="License Plate", required=True)
    vehicle_model = fields.Char(string="Vehicle Model")
    vehicle_type = fields.Selection([('car', 'Car'), ('truck', 'Truck'), ('semi-truck', 'Semi-Truck'), ('motorcycle', 'Motorcycle')])
    driver_name = fields.Char(string="Driver Name", required=True)
    odometer = fields.Float(string="Odometer Reading (km)")
    status = fields.Selection([('available', 'Available'), ('in_use', 'In Use'), ('under_maintenance', 'Under Maintenance')],string="Status", default='Available')
