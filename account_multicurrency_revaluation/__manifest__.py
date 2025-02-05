# Copyright 2012-2018 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Multicurrency revaluation",
    "version": "12.0.1.1.1",
    "category": "Finance",
    "summary": "Manage revaluation for multicurrency environment",
    "author": "Camptocamp,Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/account-closing"
               "/tree/12.0/account_multicurrency_revaluation",
    "license": 'AGPL-3',
    "depends": [
        "account",
    ],
    "demo": [
        "demo/account_demo.xml",
        "demo/currency_demo.xml",
    ],
    "data": [
        "views/res_config_view.xml",
        "security/security.xml",
        "views/account_view.xml",
        "wizard/print_currency_unrealized_report_view.xml",
        "wizard/wizard_currency_revaluation_view.xml",
        "report/assets.xml",
        "report/report.xml",
        "report/unrealized_currency_gain_loss.xml",
    ],
    'installable': True,
}
