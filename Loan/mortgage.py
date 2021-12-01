"""
This module contains classes related to Mortgages
"""

from Loan.loans import VariableRateLoan, FixedRateLoan
from Asset.house_base import House


class MortgageMixin(object):
    def __init__(self, notional, rate, start_date, end_date, home):
        if not isinstance(home, House):
            print("Error: home parameter is wrong class type")
        else:
            self._home = home
        super(MortgageMixin, self).__init__(notional, rate, start_date, end_date, home)

    def PMI(self, period):
        """Private Mortgage Insurance payment"""
        # brings in balance from the loan base class
        balance = super(MortgageMixin, self).balance(period)
        # assuming asset value = notional in this example
        LTV = balance / self._home.initial_value
        return 0.000075 * self._notional if LTV >= 0.8 else 0

    def monthly_payment(self, n=None):
        """Overrides the base monthly payment formula"""
        return super(MortgageMixin, self).monthly_payment(n) + self.PMI(n)

    def principal_due(self, n):
        """Overrides the base principal due formula"""
        # PMI comes out of principal due since it is an extra payment
        return super(MortgageMixin, self).principal_due(n) - self.PMI(n)


class VariableMortgage(MortgageMixin, VariableRateLoan):
    pass


class FixedMortgage(MortgageMixin, FixedRateLoan):
    pass
