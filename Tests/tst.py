from Loan.loan_pool import LoanPool
import numpy as np
from Tranche.tranche_base import Tranche

def check_defaults(period):
    time_periods = [10, 60, 120, 180, 210, 360]
    probabilities = [0.0005, 0.001, 0.002, 0.004, 0.002, 0.001]
    index = sum([period > r for r in time_periods])
    numbers = np.random.randint(0, 1 / probabilities[index], 2)
    return numbers


def main():
    print(check_defaults(120))
    p = Tranche(100000, 0.02, 'A')



if __name__ == '__main__':
    main()