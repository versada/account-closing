{
    "name": "Multicurrency revaluation",
    "version": "17.0.1.0.0",
    "category": "Finance",
    "summary": "Manage revaluation for multicurrency environment",
    "author": "Camptocamp, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/account-closing",
    "license": "AGPL-3",
    "depends": ["account"],
    "demo": [
        "demo/res_partner.xml",
        "demo/res_company.xml",
        "demo/res_currency_rate.xml",
        "demo/account_account.xml",
        "demo/account_journal.xml",
        "demo/account_analytic.xml",
    ],
    "data": [
        "views/res_config_settings.xml",
        "security/account_multicurrency_revaluation_groups.xml",
        "security/ir.model.access.csv",
        "views/account_account.xml",
        "views/account_move.xml",
        "views/account_move_line.xml",
        "wizard/print_currency_unrealized_report_view.xml",
        "wizard/wizard_currency_revaluation_view.xml",
        "wizard/wizard_reverse_currency_revaluation_view.xml",
        "report/currency_unrealized_report.xml",
        "templates/currency_unrealized_report.xml",
    ],
    "assets": {
        "web.report_assets_common": [
            "account_multicurrency_revaluation/static/src/css/reports.css",
        ],
    },
    "installable": True,
}
