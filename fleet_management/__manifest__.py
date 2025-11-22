{
    'name': 'Fleet Management',
    'version': '1.0',
    'summary': 'Manage vehicles, driver, fuel logs and maintenance schedule',
    'category': 'Operations/Fleet',
    'author': 'Tyson R. Pine',
    'depends': ['base', 'mail'],
    'data': [
        'views/fleet_cron_view.xml',
        'views/fleet_management_view.xml',
        'views/fleet_fuel_log_view.xml',
        'views/fleet_maintenance_log_view.xml',
        'security/ir.model.access.csv',

    ]
}