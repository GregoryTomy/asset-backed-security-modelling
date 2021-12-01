import logging
from Tranche.tranche_base import Tranche
from collections import Counter


class StandardTranche(Tranche):
    def __init__(self, notional, rate, subordination):
        super(StandardTranche, self).__init__(notional, rate, subordination)
        self._period = 0
        self._interest_shortfall = {0: 0}
        self._interestdue = {}
        self._principal_shortfall = {0: 0}

    @property
    def interest_shortfall(self):
        return self._interest_shortfall

    @property
    def interestdue(self):
        return self._interestdue

    @property
    def principal_shortfall(self):
        return self._principal_shortfall

    def toString(self):
        """Print tranche name"""
        return f'Standard Tranche {self._subordination}'

    def increase_periods(self):
        """Increases the time period by 1"""
        self._period += 1

    def make_principal_payment(self, amount):
        """Records the principal payment made for current period"""
        if self._period in self._principal_payments.keys():
            raise Exception(f'Principal payment for {self._period} has already been paid')
        elif self.notional_balance() == 0:
            self._principal_payments[self._period] = 0
            logging.debug('Balance is 0')
            return 0
        else:
            self._principal_payments[self._period] = amount

    def make_interest_payment(self, amount):
        """Records the interest payment for current period"""
        if self._period in self._interest_payments.keys():
            raise Exception(f'Interest payment for {self._period} has already been paid')
        elif self.interest_due() == 0:
            self._interest_payments[self._period] = 0
            self._interest_shortfall[self._period] = 0
            logging.debug('Interest due is 0')
        else:
            self._interest_payments[self._period] = amount
            self._interest_shortfall[self._period] = max(0, self.interest_due() - amount)

    def notional_balance(self):
        """Returns the notional balance still due for current time period"""
        total_prin_paid = sum(list(self._principal_payments.values()))
        int_shortfall = sum(list(self._interest_shortfall.values())[:self._period])
        return max(0, self.notional - total_prin_paid + int_shortfall)

    def interest_due(self):
        """Returns the interest due for a given time period"""
        if self._period == 0:
            return 0
        else:
            rate = self.monthly_rate(self.rate)
            return self.notional_balance() * rate + self._interest_shortfall[self._period - 1]

    def reset(self):
        """Resets the tranche to its original state (time 0)"""
        self._period = 0
        self._interest_shortfall = {0: 0}
        self._interestdue = {}
        self._principal_shortfall = {0: 0}
        self._principal_payments = {0: 0}
        self._interest_payments = {}
