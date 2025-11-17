from odoo import models, fields, api

class FleetVehicle(models.Model):
    _name = "fleet.management"

    name = fields.Char(string="Vehicle Name", required=True)
    license_plate = fields.Char(string="License Plate", required=True)
    vehicle_model = fields.Char(string="Vehicle Model")
    vehicle_type = fields.Selection([('car', 'Car'), ('truck', 'Truck'), ('semi-truck', 'Semi-Truck'), ('motorcycle', 'Motorcycle')])
    driver_name = fields.Char(string="Driver Name", required=True)
    odometer = fields.Float(string="Odometer Reading (km)")
    status = fields.Selection([('available', 'Available'), ('in_use', 'In Use'), ('under_maintenance', 'Under Maintenance')],string="Status", default='Available')
    fuel_log_ids = fields.One2many('fleet.fuel.log', 'vehicle_id', string="Fuel Logs", )
    total_fuel_cost = fields.Float(string="Total Fuel Cost", compute="_compute_total_fuel_cost")
    maintenance_ids = fields.One2many('fleet.maintenance.log', 'vehicle_id', string="Maintenance Record", required=True)
    total_maintenance_cost = fields.Float(string="Total Maintenance Cost", compute="_compute_total_maintenance_cost", store=True)

    @api.depends('fuel_log_ids.cost')
    def _compute_total_fuel_cost(self):
        for record in self:
            record.total_fuel_cost = sum(record.fuel_log_ids.mapped('cost'))        

    @api.depends('maintenance_ids.cost')
    def _compute_total_maintenance_cost(self):
        for record in self:
            record.total_maintenance_cost = sum(record.maintenance_ids.mapped('cost'))
            