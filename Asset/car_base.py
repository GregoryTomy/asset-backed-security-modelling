"""This module contains the Car base class"""

from Asset.asset import Asset


class Car(Asset):
    def yearly_depreciation(self):
        return 0.01


