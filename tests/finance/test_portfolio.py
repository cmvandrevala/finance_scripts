import unittest
import time

from finance.asset import Asset
from finance.portfolio import Portfolio

class PortfolioTestCase(unittest.TestCase):

    def setUp(self):
        self.portfolio = Portfolio()
        self.asset_data_1 = {"date": "2017-06-01", "name": "Proctor and Gamble", "symbol": "PG", "value": 1000, "asset_class": "Equities", "owner": "Bob", "institution": "Bank 1"}
        self.asset_data_2 = {"date": "2017-07-01", "name": "Vanguard Bond Fund", "symbol": "VTIBX", "value": 2000, "asset_class": "Fixed Income", "owner": "Sam", "institution": "Bank 2"}
        self.liability_data_1 = {"date": "2017-06-05", "name": "Visa Card", "value": 1000, "symbol": "CASHX"}
        self.liability_data_2 = {"date": "2017-07-05", "name": "Personal Loan", "value": 1500, "symbol": "CASHX"}

    def test_it_starts_off_with_no_assets_or_liabilities(self):
        self.assertEqual(self.portfolio.total_value(), 0)

    def test_it_starts_off_no_percentages(self):
        self.assertEqual(self.portfolio.percentages(), {})

    def test_it_imports_asset_data_for_a_new_asset(self):
        self.portfolio.import_data(self.asset_data_1)
        self.assertEqual(self.portfolio.percentages(), {"PG": 1.0})

    def test_it_imports_liability_data_for_a_new_liability(self):
        self.portfolio.import_data(self.liability_data_1)
        self.assertEqual(self.portfolio.total_value(), -1000)

    def test_it_imports_data_for_two_new_assets(self):
        self.portfolio.import_data(self.asset_data_1)
        self.portfolio.import_data(self.asset_data_2)
        self.assertEqual(self.portfolio.percentages(), {'PG': 0.333, 'VTIBX': 0.667})

    def test_it_imports_data_for_two_new_liabilities(self):
        self.portfolio.import_data(self.liability_data_1)
        self.portfolio.import_data(self.liability_data_2)
        self.assertEqual(self.portfolio.total_value(), -2500)

    def test_it_imports_asset_data_for_an_existing_asset(self):
        asset_data = {"date": "2017-05-01", "name": "Verizon", "symbol": "VZ", "value": 5000, "asset_class": "class", "owner": "Abraham", "institution": "Bank"}
        self.portfolio.import_data(asset_data)
        asset_data = {"date": "2017-05-02", "name": "Verizon", "symbol": "VZ", "value": 2000, "asset_class": "class", "owner": "Francis", "institution": "Bank"}
        self.portfolio.import_data(asset_data)
        self.assertEqual(self.portfolio.percentages(), {"VZ": 1.0})

    def test_it_imports_asset_data_for_existing_and_new_assets(self):
        asset_data = {"date": "2017-06-01", "name": "VZ", "symbol": "VZ", "value": 3000, "asset_class": "class", "owner": "Willie", "institution": "Bank"}
        self.portfolio.import_data(asset_data)
        asset_data = {"date": "2017-06-30", "name": "PEP", "symbol": "PEP", "value": 4000, "asset_class": "class", "owner": "Seymour", "institution": "Bank"}
        self.portfolio.import_data(asset_data)
        asset_data = {"date": "2017-06-17", "name": "VZ", "symbol": "VZ", "value": 6000, "asset_class": "class", "owner": "Jack", "institution": "Bank"}
        self.portfolio.import_data(asset_data)
        self.assertEqual(self.portfolio.percentages(), {"VZ": 0.6, "PEP": 0.4})

    def test_it_does_not_ignore_a_single_zero_dollar_amount(self):
        asset_data = {"date": "2012-01-01", "name": "T", "symbol": "T", "value": 0, "asset_class": "class", "owner": "Shauna", "institution": "Bank"}
        self.portfolio.import_data(asset_data)
        self.assertEqual(self.portfolio.percentages(), {"T": 0})

    def test_it_does_not_ignore_a_zero_dollar_amount_mixed_with_other_amounts(self):
        asset_data = {"date": "2011-02-08", "name": "Verizon", "symbol": "VZ", "value": 0, "asset_class": "class", "owner": "Brandine", "institution": "Bank"}
        self.portfolio.import_data(asset_data)
        asset_data = {"date": "2011-02-08", "name": "Something", "symbol": "SP", "value": 12.54, "asset_class": "class", "owner": "Brittney", "institution": "Bank"}
        self.portfolio.import_data(asset_data)
        self.assertEqual(self.portfolio.percentages(), {"VZ": 0, "SP": 1.0})

    def test_it_gives_the_total_value_of_the_portfolio_at_the_current_time(self):
        self.portfolio.import_data(self.asset_data_1)
        self.portfolio.import_data(self.asset_data_2)
        self.portfolio.import_data(self.liability_data_1)
        self.assertEqual(self.portfolio.total_value(), 2000)

    def test_it_gives_the_total_value_of_the_portfolio_at_a_previous_time(self):
        asset_data = {"date": "2017-01-01", "name": "Verizon", "symbol": "VZ", "value": 100, "asset_class": "class", "owner": "Carl", "institution": "Bank"}
        self.portfolio.import_data(asset_data)
        asset_data = {"date": "2017-06-01", "name": "SP", "symbol": "SP", "value": 12.50, "asset_class": "class", "owner": "Julie", "institution": "Bank"}
        self.portfolio.import_data(asset_data)
        liability_data = {"date": "2017-02-01", "name": "loan", "value": 50}
        self.portfolio.import_data(liability_data)
        self.assertEqual(self.portfolio.total_value("2017-03-01"), 50)

    def test_it_does_not_include_liabilities_in_percentages(self):
        self.portfolio.import_data(self.asset_data_1)
        self.portfolio.import_data(self.asset_data_2)
        self.portfolio.import_data(self.liability_data_1)
        self.assertEqual(self.portfolio.percentages(), {'PG': 0.333, 'VTIBX': 0.667})

    def test_it_combines_assets_with_the_same_symbol_in_percentage_calculations(self):
        asset_data = {"date": "2017-01-01", "name": "Foo", "symbol": "A", "value": 100, "asset_class": "class", "owner": "Felipe", "institution": "Bank"}
        self.portfolio.import_data(asset_data)
        asset_data = {"date": "2017-06-01", "name": "Bar", "symbol": "A", "value": 100, "asset_class": "class", "owner": "Kent", "institution": "Bank"}
        self.portfolio.import_data(asset_data)
        asset_data = {"date": "2017-02-01", "name": "Baz", "symbol": "B", "value": 100, "asset_class": "class", "owner": "Marge", "institution": "Bank"}
        self.portfolio.import_data(asset_data)
        self.assertEqual(self.portfolio.percentages(), {"A": 0.667, "B": 0.333})

    def test_it_creates_different_assets_given_different_symbols_with_the_same_name(self):
        asset_data = {"date": "2017-01-01", "name": "Foo", "symbol": "A", "value": 100, "asset_class": "class", "owner": "Lucy", "institution": "Bank"}
        self.portfolio.import_data(asset_data)
        asset_data = {"date": "2017-06-01", "name": "Foo", "symbol": "B", "value": 200, "asset_class": "class", "owner": "Greg", "institution": "Bank"}
        self.portfolio.import_data(asset_data)
        self.assertEqual(self.portfolio.percentages(), {"A": 0.333, "B": 0.667})

    def test_it_returns_zero_for_each_asset_class_if_there_is_no_asset_data(self):
        self.assertEqual(self.portfolio.asset_classes(), {"Cash Equivalents": 0, "Equities": 0, "Fixed Income": 0, "Real Estate": 0, "Commodities": 0})

    def test_it_returns_asset_data_for_one_cash_equivalent(self):
        asset_data = {"date": "2017-01-01", "name": "Foo", "symbol": "A", "value": 100, "asset_class": "Cash Equivalents", "owner": "Frank", "institution": "Bank"}
        self.portfolio.import_data(asset_data)
        self.assertEqual(self.portfolio.asset_classes(), {"Cash Equivalents": 1, "Equities": 0, "Fixed Income": 0, "Real Estate": 0, "Commodities": 0})

    def test_it_returns_asset_data_for_one_equity(self):
        self.portfolio.import_data(self.asset_data_1)
        self.assertEqual(self.portfolio.asset_classes(), {"Cash Equivalents": 0, "Equities": 1, "Fixed Income": 0, "Real Estate": 0, "Commodities": 0})

    def test_it_returns_asset_data_for_one_fixed_income_asset(self):
        self.portfolio.import_data(self.asset_data_2)
        self.assertEqual(self.portfolio.asset_classes(), {"Cash Equivalents": 0, "Equities": 0, "Fixed Income": 1, "Real Estate": 0, "Commodities": 0})

    def test_it_returns_asset_data_for_one_real_estate_asset(self):
        asset_data = {"date": "2017-01-01", "name": "Foo", "symbol": "A", "value": 100, "asset_class": "Real Estate", "owner": "Anna", "institution": "Bank"}
        self.portfolio.import_data(asset_data)
        self.assertEqual(self.portfolio.asset_classes(), {"Cash Equivalents": 0, "Equities": 0, "Fixed Income": 0, "Real Estate": 1, "Commodities": 0})

    def test_it_returns_asset_data_for_one_commodity(self):
        asset_data = {"date": "2017-01-01", "name": "Foo", "symbol": "A", "value": 100, "asset_class": "Commodities", "owner": "Clark", "institution": "Bank"}
        self.portfolio.import_data(asset_data)
        self.assertEqual(self.portfolio.asset_classes(), {"Cash Equivalents": 0, "Equities": 0, "Fixed Income": 0, "Real Estate": 0, "Commodities": 1})

    def test_it_returns_asset_data_for_two_asset_classes(self):
        asset_data = {"date": "2017-01-01", "name": "Foo", "symbol": "A", "value": 100, "asset_class": "Equities", "owner": "Tiffany", "institution": "Bank"}
        self.portfolio.import_data(asset_data)
        asset_data = {"date": "2017-02-01", "name": "Bar", "symbol": "B", "value": 100, "asset_class": "Fixed Income", "owner": "Eusavio", "institution": "Bank"}
        self.portfolio.import_data(asset_data)
        self.assertEqual(self.portfolio.asset_classes(), {"Cash Equivalents": 0, "Equities": 0.5, "Fixed Income": 0.5, "Real Estate": 0, "Commodities": 0})


if __name__ == '__main__':
    unittest.main()
