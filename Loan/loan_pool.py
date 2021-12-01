"""
This module contains the Loan Pool class
"""
from Loan.loan_base import Loan
from functools import reduce
import numpy as np


class LoanPool(object):
    def __init__(self, loans):  # loans parameter is a list of loan objects
        self._loans = loans
        self._recoveries = {}

    def __iter__(self):
        """Returns the Iterator object"""
        for i in self._loans:
            yield i


    @property
    def loans(self):
        return self._loans

    @loans.setter
    def loans(self, iloans):
        self._loans = iloans

    def active_loans(self, n):
        """Returns the number of active loans at a given period"""
        active = 0
        for i in self._loans:
            if i.balance(n) > 0:
                active += 1
        return active

    def balance(self, n):
        """Calculates the total balance for the loan pool for a given period"""
        tbal = 0
        for i in self._loans:
            tbal += i.balance(n)
        return tbal

    def principal_due(self, n):
        """Calculates the aggregate principal due in a given period"""
        tprin_due = 0
        for i in self._loans:
            tprin_due += i.principal_due(n)
        return tprin_due

    def interest_due(self, n):
        """Calculates the aggregate interest due in a given period"""
        tinterest_due = 0
        for i in self._loans:
            tinterest_due += i.interest_due(n)
        return tinterest_due

    def payment_due(self, n):
        """Calculates the payment due at a given period"""
        return self.principal_due(n) + self.interest_due(n)

    def total_principal(self):
        """Calculates the total loan principal of the loan pool"""
        tprin = 0
        for i in self._loans:
            tprin += i.notional
        return tprin


    def WAR(self):
        """Calculates the Weighted Average Rate for the loan pool"""
        sump = reduce(lambda total, i: total + (i.notional * i.rate), self.loans, 0)
        return sump / self.total_principal()

    def WAM(self):
        """Calculates the Weighted Average Maturity for the loan pool"""
        sumt = reduce(lambda total, i: total + (i.notional * i.term), self.loans, 0)
        return sumt / self.total_principal()

    def get_waterfall(self, period):
        """Return waterfall for the loan pool"""
        results = []
        # for loan in self._loans:
        #     results.append([loan.principal_due(period), loan.interest_due(period), loan.monthly_payment(period),
        #                     loan.balance(period)])

        return [period, self.principal_due(period), self.interest_due(period),
                self.payment_due(period), self._recoveries[period], self.balance(period)]

    def check_defaults(self, period):
        time_periods = [10, 60, 120, 180, 210, 360]
        probabilities = [0.0005, 0.001, 0.002, 0.004, 0.002, 0.001]
        index = sum([period > r for r in time_periods])  # (10, 60], (120, 180]
        numbers = np.random.randint(0, 1 / probabilities[index], len(self._loans))  # list of random numbers
        recoveries = sum([loan.check_default(period, number) for loan, number in zip(self._loans, numbers)])
        self._recoveries[period] = recoveries
        return recoveries

    def reset(self):
        """Reset the loans in the loan pool"""
        for i in self._loans:
            i.reset()