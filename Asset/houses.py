"""This module contains the derived House classes"""

from Asset.house_base import House


class PrimaryHome(House):
    def yearly_depreciation(self):
        return 0.09


class VacationHome(House):
    def yearly_depreciation(self):
        return 0.06
