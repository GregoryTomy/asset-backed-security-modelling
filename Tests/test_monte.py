"""This script tests out the Monte Carlo function"""

from Simulations.run_monte import run_monte
from Loan.loan_pool import LoanPool
from Asset.car_base import Car
from Loan.auto_loan import AutoLoan
from Tranche.structured_security import StructuredSecurity
import csv
from Timer.timer import Timer

loan_dict = {'Auto Loan': AutoLoan,
             'Car': Car}


def create_loan(loan_type, asset_name, asset_value, principal, rate, term):
    """Creates Loan objects from csv input"""
    loan_class = loan_dict.get(loan_type)
    asset_class = loan_dict.get(asset_name)
    loan = loan_class(float(principal), float(rate), int(term), asset_class(float(asset_value)))
    return loan


def write_to_csv(filename, input):
    """Writes the results of the waterfall to a csv file"""
    with open(str(filename), 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(input)


def main():
    loan_pool = LoanPool([])

    with open('Loans_csv.csv') as file:
        reader = csv.DictReader(file)
        for row in reader:  # create loan objects
            loan = create_loan(row.get('Loan Type'), row.get('Asset'), row.get('Asset Value'), row.get('Balance'),
                               row.get('Rate'), row.get('Term'))
            loan_pool.loans.append(loan)  # add loan to loan pool

    security = StructuredSecurity(loan_pool.total_principal(), 'Sequential')
    security.add_tranche(0.8, 0.05, 'A')
    security.add_tranche(0.2, 0.08, 'B')

    with Timer('Timer monte 1') as t:
        dirrs, als, tranche_ratings, irr = run_monte(loan_pool, security, 0.005, 10, 2)

    # time taken pre parallel processes 11.25s
    # time taken post parallel processes 6.4. Parallelization works.
    print(dirrs)
    print(als)
    print(tranche_ratings)
    print(irr)


if __name__ == '__main__':
    main()
