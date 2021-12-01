"""
This module contains the derived Loan classes
"""
from Loan.loan_base import Loan


class FixedRateLoan(Loan):
    pass


class VariableRateLoan(Loan):
    def __init__(self, notional, rate_dict, start_date, end_date, asset):
        super(VariableRateLoan, self).__init__(notional, None, start_date, end_date, asset)  # calls the base class
        # initialization
        if not isinstance(rate_dict, dict):
            print("Error: Rate parameter is not a dictionary")
        elif not all(rate_dict.values()):
            print("Error: Rates cannot be 0. Please enter correct rates")
        else:
            self._rate_dict = rate_dict

    #
    @property
    def rate_dict(self):
        return self._rate_dict

    #
    # checking if rate dictionary is actually a dictionary
    @rate_dict.setter
    def rate_dict(self, irate):
        if not isinstance(irate, dict):
            print("Error: Rate parameter is not a dictionary")
        elif not all(irate.values()):
            print("Error: Rates cannot be 0. Please enter correct rates")
        else:
            self._rate_dict = irate

    def get_rate(self, n=None):
        """Overrides the get_rate method from the Loan base class"""
        s_period = sorted([*self._rate_dict.keys()])  # created a sorted list of the periods from the rate dict
        m = [period for period in s_period if period <= n]  # generates a list of the periods less than or equal to
        # inputted period
        p = max(m)
        # returns the value for the key p
        return self._rate_dict.get(p)
