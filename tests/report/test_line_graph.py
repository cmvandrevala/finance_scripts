import unittest

from portfolio.account_builder import AccountBuilder
from portfolio.portfolio import Portfolio
from report.line_graph import LineGraph
from utilities.epoch_date_converter import EpochDateConverter


class LineGraphTestCase(unittest.TestCase):

    def setUp(self):
        self.portfolio = Portfolio()

    def test_it_returns_a_value_of_zero_on_a_single_day(self):
        line_graph = LineGraph(self.portfolio)
        net_worth_values = line_graph.net_worth_vs_time("2017-01-01", "2017-01-01")
        self.assertEqual(len(net_worth_values), 1)
        self.assertEqual(net_worth_values[0], {"x": "2017-01-01", "y": 0})

    def test_it_returns_two_values_of_zero(self):
        line_graph = LineGraph(self.portfolio)
        net_worth_values = line_graph.net_worth_vs_time("2017-06-01", "2017-06-02")
        self.assertEqual(len(net_worth_values), 2)
        self.assertEqual(net_worth_values[0], {"x": "2017-06-01", "y": 0})
        self.assertEqual(net_worth_values[1], {"x": "2017-06-02", "y": 0})

    def test_it_returns_many_values_of_zero(self):
        line_graph = LineGraph(self.portfolio)
        net_worth_values = line_graph.net_worth_vs_time("2010-09-01", "2011-08-31")
        self.assertEqual(len(net_worth_values), 365)

    def test_it_returns_the_value_of_a_single_account(self):
        account = AccountBuilder().set_name("name")\
            .set_institution("institution")\
            .set_owner("Craig")\
            .set_investment("investment")\
            .build()
        account.import_snapshot(EpochDateConverter().date_to_epoch("2005-12-10"), 1000)
        self.portfolio.import_account(account)
        line_graph = LineGraph(self.portfolio)
        net_worth_values = line_graph.net_worth_vs_time("2005-12-09", "2005-12-11")
        self.assertEqual(net_worth_values[0], {"x": "2005-12-09", "y": 0})
        self.assertEqual(net_worth_values[1], {"x": "2005-12-10", "y": 1000})
        self.assertEqual(net_worth_values[2], {"x": "2005-12-11", "y": 1000})

    def test_it_returns_the_value_of_two_accounts(self):
        account_one = AccountBuilder().set_name("name")\
            .set_institution("institution")\
            .set_owner("Craig")\
            .set_investment("investment")\
            .build()
        account_two = AccountBuilder().set_name("name")\
            .set_institution("institution")\
            .set_owner("Samuel")\
            .set_investment("investment")\
            .set_liability()\
            .build()
        account_one.import_snapshot(EpochDateConverter().date_to_epoch("2009-10-15"), 10)
        account_two.import_snapshot(EpochDateConverter().date_to_epoch("2009-10-17"), 1000)
        self.portfolio.import_account(account_one)
        self.portfolio.import_account(account_two)
        line_graph = LineGraph(self.portfolio)
        net_worth_values = line_graph.net_worth_vs_time("2009-10-13", "2009-10-19")
        self.assertEqual(net_worth_values[0], {"x": "2009-10-13", "y": 0})
        self.assertEqual(net_worth_values[1], {"x": "2009-10-14", "y": 0})
        self.assertEqual(net_worth_values[2], {"x": "2009-10-15", "y": 10})
        self.assertEqual(net_worth_values[3], {"x": "2009-10-16", "y": 10})
        self.assertEqual(net_worth_values[4], {"x": "2009-10-17", "y": -990})
        self.assertEqual(net_worth_values[5], {"x": "2009-10-18", "y": -990})
        self.assertEqual(net_worth_values[6], {"x": "2009-10-19", "y": -990})