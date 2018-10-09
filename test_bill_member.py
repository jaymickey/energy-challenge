import unittest
from unittest.mock import patch
from bill_member import calculate_bill
from test_data import (
    multiple_sources_data, multiple_accounts_data, multiple_accounts_data_2)


class TestBillMember(unittest.TestCase):

    def test_calculate_bill_for_august(self):
        amount, kwh = calculate_bill(member_id='member-123',
                                     account_id='ALL',
                                     bill_date='2017-08-31')
        self.assertEqual(amount, 27.57)
        self.assertEqual(kwh, 167)

    def test_calculate_bill_with_gas_for_august(self):
        mock_get_readings = patch(
            'load_readings.get_readings', return_value=multiple_sources_data)
        mock_get_readings.start()
        amount, kwh = calculate_bill(member_id='member-123',
                                     account_id='ALL',
                                     bill_date='2017-08-31')
        self.assertEqual(amount, 54.56)
        self.assertEqual(kwh, 677)
        mock_get_readings.stop()

    def test_calculate_with_multiple_accounts_for_august(self):
        mock_get_readings = patch(
            'load_readings.get_readings', return_value=multiple_accounts_data)
        mock_get_readings.start()
        amount, kwh = calculate_bill(member_id='member-123',
                                     account_id='ALL',
                                     bill_date='2017-08-31')
        self.assertEqual(amount, 55.14)
        self.assertEqual(kwh, 334)
        mock_get_readings.stop()

    def test_calculate_single_account_with_multiple_accounts_for_august(self):
        mock_get_readings = patch(
            'load_readings.get_readings', return_value=multiple_accounts_data_2)
        mock_get_readings.start()
        amount, kwh = calculate_bill(member_id='member-123',
                                     account_id='account-abc',
                                     bill_date='2017-08-31')
        self.assertEqual(amount, 27.57)
        self.assertEqual(kwh, 167)
        mock_get_readings.stop()


if __name__ == '__main__':
    unittest.main()
