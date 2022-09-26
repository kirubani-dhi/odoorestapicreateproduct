# License: LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl)
{
    "name": "ODOO REST API - Product Create",
    "version": "1.0.1",
    "category": "REST API",
    "summary": "ODOO REST API - Product Create",
    'author': 'KJ',
    'license': 'LGPL-3',
    "description": """ ODOO REST API - Product Create
    ====================
    Product create from middleware to odd while hitting the Postman URL,
    With use of this module user can enable REST API in any Odoo applications/modules.
    
    """,
    "depends": ["base","web","sale","stock","product"],
    "data": ["data/ir_config_param.xml", 
             "views/ir_model.xml", 
             "views/res_users.xml", 
             "security/ir.model.access.csv"
        ],
    "images": ["static/description/main_screenshot.png"],
    'installable': True,
    'applicable': True,
    'auto_install': False,
    'price': 10.00,
    'currency': 'EUR',
    "live_test_url":'https://www.youtube.com/watch?v=Vfqt7wq11pM'
}
