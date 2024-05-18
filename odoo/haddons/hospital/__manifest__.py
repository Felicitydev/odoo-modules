{
    'name' : 'Hospital Management',
    'version' : '1.0.0',
    'summary': 'Hospital Management System',
    'author': 'Félicité TEGHOMO',
    'sequence': -100,
    'description': """Hospital Management System""",
    'category': 'Hospital',
    'depends' : ['mail'],
    'data': [
        'security/ir.model.access.csv',
        'views/patient.xml',
        'views/female_patient.xml',
        'views/menu.xml',

    ],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
    'assets': {},
    'license': 'LGPL-3',
}
