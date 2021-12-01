"""
This module contains the basic Loan Class
"""
from Asset.asset import Asset
import logging
from functools import wraps
import numpy as np


def memoize(f):
    """Memoize the result of a function"""
    memory = {}

    @wraps(f)
    def wrapped(*args, **kwargs):
        key = str(args) + str(kwargs)
        if key not in memory:
            memory[key] = f(*args, **kwargs)
        return memory[key]

    return wrapped


class Loan(object):

    def __init__(self, notional, rate, term, asset):
        self._notional = notional
        self._term = term
        if rate == 0:
            logging.error(f'Error: {rate} was entered. Rate cannot be 0 ')
            raise ValueError("Rate cannot be 0. Please enter correct rate.")
        else:
            self._rate = rate
        if not isinstance(asset, Asset):
            logging.error(f'Error: Asset type {type(asset)} entered is incorrect. Asset must be of "Asset" type')
            raise TypeError("Error: Asset parameter is wrong class type")
        else:
            self._asset = asset
        self._default_flag = 0

    # getter/setter property functions
    @property
    def notional(self):
        return self._notional

    @notional.setter
    def notional(self, inotional):
        self._notional = inotional

    @property
    def rate(self):
        return self._rate

    @rate.setter
    def rate(self, irate):
        if irate == 0:
            logging.error(f'Error: {irate} was entered. Rate cannot be 0 ')
            raise ValueError("Rate cannot be 0. Please enter correct rate.")
        else:
            self._rate = irate

    # adjusting term property
    @property
    def term(self):
        return self._term

    @term.setter
    def term(self, iterm):
        self._term = iterm

    # asset parameter getter/setter
    @property
    def asset(self):
        return self._asset

    @asset.setter
    def asset(self, iasset):
        if not isinstance(iasset, Asset):
            logging.error(f'Error: Asset type {type(iasset)} entered is incorrect. Asset must be of "Asset" type')
            raise TypeError("Error: asset parameter is wrong class type")
        else:
            self._asset = iasset

    @staticmethod
    def monthly_rate(rate):
        """Converts annual interest rate to monthly rate"""
        return rate / 12

    @staticmethod
    def annual_rate(rate_monthly):
        """Converts monthly interest rate to annual rate"""
        return (1 + rate_monthly) ** 12 - 1

    def monthly_payment(self, n=None):
        """Calculates the monthly payment"""
        if n == 0:
            return 0
        else:
            rate = self.get_rate(n)
            if not self.paid_off(self.term, n):
                return (self._default_flag == 0) * self.calc_monthly_pmt(self._notional, rate, self.term)
                # False = 0, True = 1
            else:
                return 0

    def total_payment(self):
        """Total payments over the entire term of the loan"""
        total = self.monthly_payment() * self.term
        logging.debug(f'total payment is {total}')
        return total

    def total_interest(self):
        """Calculates the total interest over the entire term of the loan"""
        # total interest paid over the life of the loan is the total payments made minus
        # the initial principal amount
        total = self.total_payment() - self._notional
        logging.debug(f'total interest is {total}')
        return total

    def balance(self, n):
        """Calculates the remaining balance at period n"""
        rate = self.get_rate(n)
        return (self._default_flag == 0) * self.calc_balance(self._notional, rate, self.term, n)

    def interest_due(self, n):
        """Calculates the interest due at period n"""
        rate = Loan.monthly_rate(self.get_rate(n))
        if n == 0:
            return 0
        else:
            interest = rate * self.balance(n - 1)
            logging.debug(f'interest due at period {n} is {interest}')
            return (self._default_flag == 0) * interest

    def principal_due(self, n):
        """Calculates the principal due at period n"""
        if n == 0:
            return 0
        else:
            prin = self.monthly_payment(n) - self.interest_due(n)
            logging.debug(f'Principal due at period {n} is {prin}')
            return prin

    # Recursive versions of the same three methods
    @memoize
    def balance_rec(self, n):
        """Calculates the remaining balance at period n recursively"""
        if n == 0:
            logging.warning('Recursive versions are expected to take longer. Explicit functions are recommended')
            return self._notional
        else:
            return self.balance_rec(n - 1) - self.principal_due(n)

    @memoize
    def principal_due_rec(self, n):
        """Calculates the principal due at period n recursively"""
        return self.monthly_payment() - self.interest_due_rec(n)

    @memoize
    def interest_due_rec(self, n):
        """Calculates the interest due at period n recursively"""
        rate = Loan.monthly_rate(self._rate)
        return rate * self.balance_rec(n - 1)

    def get_rate(self, n=None):
        """Returns a rate for a given period"""
        return self._rate

    def recovery_value(self, n):
        """Returns the recovery value of an asset for a given period"""
        r = self._asset.value(n) * 0.6
        logging.debug(f'Recovery value at period {n} is {r}')
        return r

    def equity(self, n):
        """Returns the remaining equity available at a given period"""
        e = self._asset.value(n) - self.balance(n)
        logging.debug(f'Equity value at period {n} is {e}')
        return e

    def check_default(self, period, value):
        """Determines whether a loan defaults"""
        if value == 0:
            self._default_flag = 1
            return self.recovery_value(period)
        else:
            return 0

    def reset(self):
        """Resets default flag to 0 for simulations"""
        self._default_flag = 0

    # class level methods

    @classmethod
    def calc_monthly_pmt(cls, face, rate, term):
        """Calculates the monthly payment at the class level"""
        # calculating the monthly rate using static-level method
        monthly_rate = Loan.monthly_rate(rate)
        pmt = (monthly_rate * face) / (1 - (1 + monthly_rate) ** (-term))
        logging.debug(f'monthly payment is {pmt}')
        return pmt

    @classmethod
    def calc_balance(cls, face, rate, term, period):
        """Calculates the balance at period in at the class level"""
        monthly_rate = Loan.monthly_rate(rate)
        if period > term:
            logging.info(f'period {period} is greater than {term}')
            return 0
        else:
            bal = (face * (1 + monthly_rate) ** period) - cls.calc_monthly_pmt(face, rate, term) * \
                  ((1 + monthly_rate) ** period - 1) / monthly_rate
            logging.debug(f'balance is {bal}')
        return max(0, bal)

    @classmethod
    def paid_off(cls, term, period):
        po = False
        if period > term:
            po = True
        return po
