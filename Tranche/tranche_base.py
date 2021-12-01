"""This module contains the abstract Tranche base class"""
import logging
import numpy_financial as npf
import numpy as np
from collections import Counter


class Tranche(object):
    DIRR_bps = np.array([-np.inf, 0.06, 0.67, 1.3, 2.7, 5.2, 8.9, 13, 19,
                         27, 46, 72, 106, 143, 183, 231, 311, 2500, 10000])
    letter_ratings = ["Aaa", "Aa1", "Aa2", "Aa3", "A1", "A2", "A3", "Baa1", "Baa2",
                      "Baa3", "Ba1", "Ba2", "Ba3", "B1", "B2", "B3", "Caa", "Ca"]

    def __init__(self, notional, rate, subordination):
        if isinstance(notional, (float, int)):
            self._notional = notional
        else:
            logging.error('Notional must be a number')
        if isinstance(rate, float) and rate < 1:
            self._rate = rate
        else:
            logging.error('Rate must be a Float and less than 1')
        self._subordination = subordination
        self._principal_payments = {0: 0}
        self._interest_payments = {}

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
        self._rate = irate

    @property
    def subordination(self):
        return self._subordination

    @subordination.setter
    def subordination(self, isub):
        self._subordination = isub

    @property
    def principal_payments(self):
        return self._principal_payments

    @property
    def interest_payments(self):
        return self._interest_payments

    @staticmethod
    def monthly_rate(rate):
        """Calculates the monthly rate based on given annual rate"""
        return rate / 12

    def toString(self):
        raise NotImplementedError()

    def IRR(self):
        """Returns in internal rate of return for the tranche"""
        cdict = Counter(self._principal_payments) + Counter(self._interest_payments)
        clist = list(dict(cdict).values())
        clist.insert(0, -self._notional)
        return npf.irr(clist) * 12

    def DIRR(self):
        """Returns the reduction in yield"""
        dirr = self._rate - self.IRR()
        return round(dirr, 2)

    def AL(self):
        """Returns the average life of the tranche"""
        sum_product = [x * y for x, y in enumerate(self._principal_payments.values())]
        total_prin_payments = sum(self._principal_payments.values())
        if abs(total_prin_payments - self._notional) > 0:  # if principal is not paid down
            return np.NaN
        else:
            return round(sum(sum_product) / self._notional, 2)

    @classmethod
    def abs_rating(cls, dirr):
        """Returns the ABS rating for a given DIRR"""
        index = np.where(cls.DIRR_bps >= dirr * 10000.0)[0][0] - 1
        return cls.letter_ratings[index]

