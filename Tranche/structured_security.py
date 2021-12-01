"""
This module contains the Structured Security class
"""

from Tranche.standard_tranche import StandardTranche


class StructuredSecurity(object):
    def __init__(self, total_notional, mode):
        self._total_notional = total_notional
        self._mode = mode
        self._tranches = []  # internal list of tranches
        self._loanpool = None  # bring in loan pool from assets for principal received
        self._period = 0
        self._reserve_account = 0
    @property
    def total_notional(self):
        return self._total_notional

    @property
    def mode(self):
        return self._mode

    @property
    def tranches(self):
        return self._tranches

    @property
    def reserve_account(self):
        return self._reserve_account

    @property
    def loanpool(self):
        return self._loanpool

    @loanpool.setter
    def loanpool(self, iloanpool):
        self._loanpool = iloanpool

    @property
    def period(self):
        return self._period

    def get_rates(self):
        """Returns list of tranche rates"""
        return [tranche.rate for tranche in self._tranches]

    def get_notionals(self):
        """Returns list of tranche notionals"""
        return [tranche.notional for tranche in self._tranches]

    def add_tranche(self, percent_notional, rate, subordination):
        """Adds tranches to the object"""
        # instantiate tranche with percent of total notional
        tranche = StandardTranche(percent_notional * self._total_notional, rate, subordination)
        self._tranches.append(tranche)  # add tranche to internal list of tranches
        self._tranches.sort(key=lambda x: x.subordination)  # sort tranche list based on subordination

    def increase_period(self):
        self._period += 1
        for tranche in self._tranches:
            tranche.increase_periods()

    def make_payments(self, amount):
        """Cycles through and pays the tranches"""
        cash_available = amount + self._reserve_account

        # Interest payment calculations
        for tranche in self._tranches:
            interest_due = tranche.interest_due()  # ask tranche how much interest is owed
            tranche.interestdue[self._period] = interest_due  # record the interest owed for the period
            interest_paid = min(cash_available, interest_due)
            tranche.make_interest_payment(interest_paid)
            cash_available -= interest_paid  # calculate remaining cash available

        prin_recieved = self._loanpool.principal_due(self._period)  # get total principal received from loan pool
        # Principal payment calculations
        if self._mode == 'Sequential':
            for tranche in self._tranches:
                prin_recieved += tranche.principal_shortfall[self._period - 1]
                balance = tranche.notional_balance()
                prin_due = min(balance, prin_recieved)
                prin_paid = min(cash_available, prin_due)
                tranche.make_principal_payment(prin_paid)  # make the payment
                tranche.principal_shortfall[self._period] = max(0, prin_due - prin_paid)
                prin_recieved -= prin_paid  # reduce prin
                cash_available -= prin_paid # reduce total cash available
        elif self._mode == 'Pro Rata':
            total_prin_paid = 0
            for tranche in self._tranches:
                prin_recieved += tranche.principal_shortfall[self._period - 1]
                percent = tranche.notional / self._total_notional
                balance = tranche.notional_balance()
                prin_due = min(balance, prin_recieved * percent)
                prin_paid = min(cash_available, prin_due)
                tranche.make_principal_payment(prin_paid)  # make the payment
                tranche.principal_shortfall[self._period] = max(0, prin_due - prin_paid)
                total_prin_paid += prin_paid

                # prin_recieved -= prin_paid
            cash_available -= total_prin_paid
        self._reserve_account = cash_available

    # def add_cashflows(self):
    #     for tranche in self._tranches:
    #         cdict = Counter(tranche.principal_payments) + Counter(tranche.interest_payments)
    #         clist = list(dict(cdict).values())
    #         tranche.cashflows.extend(clist)

    def get_waterfall(self, period):
        """Get tranche waterfall"""
        waterfall = [[period]]
        for tranche in self._tranches:
            waterfall.append([tranche.interestdue[period], tranche.interest_payments[period],
                              tranche.interest_shortfall[period], tranche.principal_payments[period],
                              tranche.notional_balance()])
        waterfall.append([self._reserve_account])
        return waterfall

    def reset(self):
        self._reserve_account = 0
        self._period = 0
        for i in self._tranches:
            i.reset()
