"""
This module contains the basic Asset Class
"""


class Asset(object):
    def __init__(self, initial_value):
        self._initial_value = initial_value

    @property
    def initial_value(self):
        return self._initial_value

    @initial_value.setter
    def initial_value(self, input_initial_value):
        self._initial_value = input_initial_value

    def yearly_depreciation(self):
        """Returns a yearly depreciation rate (hardcoded here)"""
        raise NotImplementedError

    def monthly_depreciation(self):
        """Returns the monthly depreciation rate for given annual depreciation rate"""
        return self.yearly_depreciation() / 12

    def value(self, t):
        """Calculates the current value of the asset for a given period t"""
        return self._initial_value * (1 - self.monthly_depreciation()) ** t

