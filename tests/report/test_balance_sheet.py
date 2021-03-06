import unittest

from portfolio.account_builder import AccountBuilder
from portfolio.portfolio import Portfolio
from report.balance_sheet import BalanceSheet
from utilities.constants import Constants
from utilities.epoch_date_converter import EpochDateConverter


class BalanceSheetTestCase(unittest.TestCase):
    def setUp(self):
        self.asset = AccountBuilder().set_name("name") \
            .set_owner("owner") \
            .set_investment("investment") \
            .set_institution("institution") \
            .set_update_frequency(3) \
            .build()
        self.liability = AccountBuilder().set_name("name") \
            .set_owner("owner") \
            .set_investment("investment") \
            .set_institution("institution") \
            .set_liability() \
            .build()
        self.portfolio = Portfolio()

    def test_it_returns_a_formatted_row_for_a_balance_sheet(self):
        date_difference = Constants.SECONDS_PER_DAY * 2
        timestamp = EpochDateConverter().date_to_epoch()
        expected_date = EpochDateConverter().epoch_to_date(timestamp - date_difference)
        self.asset.import_snapshot(timestamp - date_difference, 100)
        balance_sheet_row = BalanceSheet().row(self.asset)
        self.assertEqual(balance_sheet_row, [expected_date, "institution", "name", "investment", "owner", "100.00"])

    def test_it_returns_an_empty_balance_sheet_if_there_are_no_accounts_in_the_portfolio(self):
        balance_sheet = BalanceSheet(self.portfolio)
        expected_output = [["---", "---", "---", "---", "---", "---"],
                           ["", "", "", "", "Total", "0.00"]]
        self.assertEqual(balance_sheet.create(), expected_output)

    def test_it_returns_a_balance_sheet_with_one_asset(self):
        self.asset.import_snapshot(EpochDateConverter().date_to_epoch('2017-12-12'), 100)
        self.portfolio.import_account(self.asset)
        balance_sheet = BalanceSheet(self.portfolio)
        expected_output = [["2017-12-12", "institution", "name", "investment", "owner", "100.00"],
                           ["---", "---", "---", "---", "---", "---"],
                           ["", "", "", "", "Total", "100.00"]]
        self.assertEqual(balance_sheet.create(), expected_output)

    def test_it_returns_a_balance_sheet_with_one_liability(self):
        self.liability.import_snapshot(EpochDateConverter().date_to_epoch('2011-1-1'), 500.12)
        self.portfolio.import_account(self.liability)
        balance_sheet = BalanceSheet(self.portfolio)
        expected_output = [["---", "---", "---", "---", "---", "---"],
                           ["2011-01-01", "institution", "name", "investment", "owner", "500.12"],
                           ["", "", "", "", "Total", "-500.12"]]
        self.assertEqual(balance_sheet.create(), expected_output)

    def test_it_returns_a_balance_sheet_with_an_asset_and_a_liability(self):
        self.asset.import_snapshot(EpochDateConverter().date_to_epoch('2017-11-12'), 1020)
        self.liability.import_snapshot(EpochDateConverter().date_to_epoch('2013-5-5'), 0.12)
        self.portfolio.import_account(self.asset)
        self.portfolio.import_account(self.liability)
        balance_sheet = BalanceSheet(self.portfolio)
        expected_output = [["2017-11-12", "institution", "name", "investment", "owner", "1020.00"],
                           ["---", "---", "---", "---", "---", "---"],
                           ["2013-05-05", "institution", "name", "investment", "owner", "0.12"],
                           ["", "", "", "", "Total", "1019.88"]]
        self.assertEqual(balance_sheet.create(), expected_output)

    def test_it_returns_no_assets_or_liabilities(self):
        balance_sheet = BalanceSheet(self.portfolio)
        expected_output = {"assets": [], "liabilities": []}
        self.assertEqual(balance_sheet.json(), expected_output)

    def test_it_returns_an_asset(self):
        self.asset.import_snapshot(EpochDateConverter().date_to_epoch('2017-11-12'), 1020)
        self.portfolio.import_account(self.asset)
        balance_sheet = BalanceSheet(self.portfolio)
        expected_output = {"assets": [{"lastUpdated": "2017-11-12T12:00:00-05:00", "institution": "institution", "owner": "owner", "account": "name", "value": 1020, "investment": "investment"}], "liabilities": []}
        self.assertEqual(balance_sheet.json(), expected_output)

    def test_it_returns_two_assets(self):
        asset_one = AccountBuilder().set_name("name one") \
            .set_owner("owner one") \
            .set_investment("investment one") \
            .set_institution("institution one") \
            .set_update_frequency(5) \
            .build()
        asset_two = AccountBuilder().set_name("name two") \
            .set_owner("owner two") \
            .set_investment("investment two") \
            .set_institution("institution two") \
            .set_update_frequency(3) \
            .build()
        asset_one.import_snapshot(EpochDateConverter().date_to_epoch('2005-11-12'), 100.50)
        asset_two.import_snapshot(EpochDateConverter().date_to_epoch('2000-12-12'), 1289)
        self.portfolio.import_account(asset_one)
        self.portfolio.import_account(asset_two)
        balance_sheet = BalanceSheet(self.portfolio)
        expected_output = {"assets": [{"lastUpdated": "2005-11-12T12:00:00-05:00", "institution": "institution one", "owner": "owner one", "account": "name one", "value": 100.50, "investment": "investment one"}, {"lastUpdated": "2000-12-12T12:00:00-05:00", "institution": "institution two", "owner": "owner two", "account": "name two", "value": 1289, "investment": "investment two"}], "liabilities": []}
        self.assertEqual(balance_sheet.json(), expected_output)

    def test_it_returns_a_liability(self):
        self.liability.import_snapshot(EpochDateConverter().date_to_epoch('2010-01-10'), 129)
        self.portfolio.import_account(self.liability)
        balance_sheet = BalanceSheet(self.portfolio)
        expected_output = {"assets": [], "liabilities": [{"lastUpdated": "2010-01-10T12:00:00-05:00", "institution": "institution", "owner": "owner", "account": "name", "value": 129, "investment": "investment"}]}
        self.assertEqual(balance_sheet.json(), expected_output)

    def test_it_returns_two_liabilities(self):
        liability_one = AccountBuilder().set_name("name one") \
            .set_owner("owner one") \
            .set_investment("investment one") \
            .set_institution("institution one") \
            .set_update_frequency(5) \
            .set_liability() \
            .build()
        liability_two = AccountBuilder().set_name("name two") \
            .set_owner("owner two") \
            .set_investment("investment two") \
            .set_institution("institution two") \
            .set_update_frequency(3) \
            .set_liability() \
            .build()
        liability_one.import_snapshot(EpochDateConverter().date_to_epoch('2005-11-12'), 100.50)
        liability_two.import_snapshot(EpochDateConverter().date_to_epoch('2000-12-12'), 1289)
        self.portfolio.import_account(liability_one)
        self.portfolio.import_account(liability_two)
        balance_sheet = BalanceSheet(self.portfolio)
        expected_output = {"assets": [], "liabilities": [{"lastUpdated": "2005-11-12T12:00:00-05:00", "institution": "institution one", "owner": "owner one", "account": "name one", "value": 100.50, "investment": "investment one"}, {"lastUpdated": "2000-12-12T12:00:00-05:00", "institution": "institution two", "owner": "owner two", "account": "name two", "value": 1289, "investment": "investment two"}]}
        self.assertEqual(balance_sheet.json(), expected_output)

if __name__ == '__main__':
    unittest.main()
