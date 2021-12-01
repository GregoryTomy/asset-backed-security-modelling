"""This module contains the derived Car types"""

from Asset.car_base import Car


class Lambourghini(Car):
    def yearly_depreciation(self):
        return 0.01


class Lexus(Car):
    def yearly_depreciation(self):
        return 0.06
