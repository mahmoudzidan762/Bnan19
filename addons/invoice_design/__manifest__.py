{
    'name': 'Invoice Report Design',
    'version': '1.0',
    'summary': 'Custom Invoice Report Design',
    'description': """ """,
    'author': 'Dgprojx',
    'depends': [
        'base', 'account', 'l10n_sa', 'l10n_sa_edi'],
    'data': [
        'security/ir.model.access.csv',
        'reports/invoice_report.xml',
        'views/custom_invoice_template_view.xml',
        'views/res_partner_inherit.xml',
        'views/account_move_inherit.xml',
    ],

    'demo': [],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
