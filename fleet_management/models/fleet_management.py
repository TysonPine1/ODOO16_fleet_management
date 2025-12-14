from odoo import models, fields, api

class FleetVehicle(models.Model):
    _name = "fleet.management"

    name = fields.Char(string="Vehicle Name", required=True)
    license_plate = fields.Char(string="License Plate", required=True)
    vehicle_model = fields.Char(string="Vehicle Model")
    driver_name = fields.Many2one('res.partner', string="Driver Name", required=True)

    vehicle_type = fields.Selection([('car', 'Car'), ('truck', 'Truck'), ('semi-truck', 'Semi-Truck'), ('motorcycle', 'Motorcycle')])
    odometer = fields.Float(string="Odometer Reading (km)")
    status = fields.Selection([('available', 'Available'), ('in_use', 'In Use'), ('under_maintenance', 'Under Maintenance')],string="Status", default='available')

    fuel_log_ids = fields.One2many('fleet.fuel.log', 'vehicle_id', string="Fuel Logs", )
    maintenance_ids = fields.One2many('fleet.maintenance.log', 'vehicle_id', string="Maintenance Record", required=True)

    total_fuel_cost = fields.Float(string="Total Fuel Cost", compute="_compute_total_fuel_cost")
    total_maintenance_cost = fields.Float(string="Total Maintenance Cost", compute="_compute_total_maintenance_cost", store=True)
    total_expense = fields.Float(string="Total Expense", compute="_compute_total_expense", store=True)

    maintenance_due = fields.Boolean(string="Maintenance Due", compute="_compute_maintenance_due", store=True)

    @api.depends('fuel_log_ids.fuel_cost')
    def _compute_total_fuel_cost(self):
        for record in self:
            record.total_fuel_cost = sum(record.fuel_log_ids.mapped('fuel_cost'))        

    @api.depends('maintenance_ids.maintenance_cost')
    def _compute_total_maintenance_cost(self):
        for record in self:
            record.total_maintenance_cost = sum(record.maintenance_ids.mapped('maintenance_cost'))
    
    @api.depends('total_fuel_cost', 'total_maintenance_cost')
    def _compute_total_expense(self):
        for record in self:
            record.total_expense = record.total_fuel_cost + record.total_maintenance_cost
    

@api.depends('maintenance_ids.next_due_date', 'maintenance_ids.state')
def _compute_maintenance_due(self):
    today = fields.Date.today()
    for record in self:
        record.maintenance_due = any(
            log.state == 'scheduled'
            and log.next_due_date
            and log.next_due_date <= today
            for log in record.maintenance_ids
        )

    # @api.depends('maintenance_ids.next_due_date', 'maintenance_ids.state')
    # def _compute_maintenance_due(self):
    #     today = fields.Date.today()
    #     for record in self:
    #         record.maintenance_due = any(
    #             log.state == 'scheduled' and log.next_due_date and log.next_due_date <= today
    #             for log in record.maintenance_ids
    #         )