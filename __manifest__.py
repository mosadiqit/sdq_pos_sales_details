# -*- coding: utf-8 -*-
{
    'name': "sdq_pos_sales_details",

    'summary': """
        This model adds more details about pos sales """,


    'author': "Mohamed Sadiq",
    'website': "http://www.sadiq.ma",

    # Categories can be used to filter modules in modules listing
    # for the full list
    'category': 'project Managements',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'point_of_sale', 'product', 'mail', 'uom', 'stock'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'report/report.xml',
        'report/pos_report.xml',

    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}