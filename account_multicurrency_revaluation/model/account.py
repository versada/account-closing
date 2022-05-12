# Copyright 2012-2018 Camptocamp SA
# Copyright 2020 CorporateHub (https://corporatehub.eu)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class AccountAccountLine(models.Model):
    _inherit = "account.move.line"
    # By convention added columns start with gl_.
    gl_foreign_balance = fields.Float(string="Aggregated Amount currency")
    gl_balance = fields.Float(string="Aggregated Amount")
    gl_revaluated_balance = fields.Float(string="Revaluated Amount")
    gl_currency_rate = fields.Float(string="Currency rate")


class AccountAccount(models.Model):
    _inherit = "account.account"

    currency_revaluation = fields.Boolean(
        string="Allow currency revaluation",
    )

    _sql_mapping = {
        'balance':
            "COALESCE(SUM(debit),0) - COALESCE(SUM(credit), 0) as balance",
        'debit': "COALESCE(SUM(debit), 0) as debit",
        'credit': "COALESCE(SUM(credit), 0) as credit",
        'foreign_balance':
            "COALESCE(SUM(amount_currency), 0) as foreign_balance",
    }

    def init(self):
        # all receivable, payable, Bank and Cash accounts should
        # have currency_revaluation True by default
        res = super().init()
        accounts = self.env["account.account"].search(
            [
                ("user_type_id.id", "in", self._get_revaluation_account_types()),
                ("currency_revaluation", "=", False),
            ]
        )
        accounts.write({"currency_revaluation": True})
        return res

    def _get_revaluation_account_types(self):
        return [
            self.env.ref("account.data_account_type_receivable").id,
            self.env.ref("account.data_account_type_payable").id,
            self.env.ref("account.data_account_type_liquidity").id,
        ]

    @api.onchange("user_type_id")
    def _onchange_user_type_id(self):
        revaluation_accounts = self._get_revaluation_account_types()
        for rec in self:
            if rec.user_type_id.id in revaluation_accounts:
                rec.currency_revaluation = True

    def _revaluation_query(self, revaluation_date):
        tables, where_clause, where_clause_params = \
            self.env['account.move.line']._query_get()

        query = """
WITH amount AS (
    SELECT
        aml.account_id,
        CASE WHEN aat.type IN ('payable', 'receivable')
            THEN aml.partner_id
            ELSE NULL
        END AS partner_id,
        aml.currency_id,
        aml.debit,
        aml.credit,
        aml.amount_currency
    FROM account_move_line aml
    INNER JOIN account_account acc ON aml.account_id = acc.id
    INNER JOIN account_account_type aat ON acc.user_type_id = aat.id
    WHERE
        aml.account_id IN %s
        AND aml.date <= %s
        AND aml.currency_id IS NOT NULL
        AND aml.parent_state='posted'
    GROUP BY
        aat.type,
        aml.id
)
SELECT
    account_id as id,
    partner_id,
    currency_id,
""" + ', '.join(self._sql_mapping.values()) + """
FROM amount
""" + (('WHERE ' + where_clause) if where_clause else '') + """
GROUP BY account_id, currency_id, partner_id
        """

        params = [
            tuple(self.ids),
            revaluation_date,
            *where_clause_params,
        ]

        return query, params

    def compute_revaluations(self, revaluation_date):
        query, params = self._revaluation_query(revaluation_date)
        self.env.cr.execute(query, params)
        lines = self.env.cr.dictfetchall()

        data = {}
        for line in lines:
            account_id, currency_id, partner_id = \
                line['id'], line['currency_id'], line['partner_id']
            data.setdefault(account_id, {})
            data[account_id].setdefault(partner_id, {})
            data[account_id][partner_id].setdefault(currency_id, {})
            data[account_id][partner_id][currency_id] = line
        return data


class AccountMove(models.Model):
    _inherit = "account.move"

    revaluation_to_reverse = fields.Boolean(
        string="revaluation to reverse", default=False
    )
