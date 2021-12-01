"""
This module contains the Fixed Auto Loan class
"""
from Loan.loans import FixedRateLoan
from Asset.car_base import Car


class AutoLoan(FixedRateLoan):
    def __init__(self, notional, rate, term, car):
        super(AutoLoan, self).__init__(notional, rate, term, car)
        if not isinstance(car, Car):
            print("Error: car parameter is wrong class type")
        else:
            self._car = car
