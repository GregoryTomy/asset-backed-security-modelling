"""
This script contains the stand alone Waterfall function
"""

from Loan.loan_pool import LoanPool
from Tranche.structured_security import StructuredSecurity


def do_waterfall(loanpool, structuredsecurity):
    period = 0
    lp_waterfalls = []
    ss_waterfalls = []

    while loanpool.active_loans(period):  # False when active loans is 0 (Falsey value)
        structuredsecurity.increase_period()
        period += 1
        structuredsecurity.loanpool = loanpool
        recovery_amount = loanpool.check_defaults(period)
        total_payment = loanpool.payment_due(period) + recovery_amount  # ask the loanpool for its total payment for
        # current period
        structuredsecurity.make_payments(total_payment)  # pay structured securities
        # get waterfall details and append to variable
        lp_waterfalls.append(loanpool.get_waterfall(period))
        ss_waterfalls.append(structuredsecurity.get_waterfall(period))

    # save tranche DIRR and ALL as a list in metrics
    metrics = [[tranche.IRR(), tranche.DIRR(), tranche.AL()] for tranche in structuredsecurity.tranches]

    # print(f'Tranche {tranche.subordination} IRR: {tranche.IRR(): .2f}')
    # print(
    #     f'Tranche {tranche.subordination} DIRR: {tranche.DIRR(): .0f} and Rating {tranche.abs_rating(tranche.DIRR())}')
    # print(f'Tranche {tranche.subordination} AL: {tranche.AL()}')

    return [lp_waterfalls, ss_waterfalls, metrics]
