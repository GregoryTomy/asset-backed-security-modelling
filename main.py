"""This script demonstrates the simulation functions with parallelization"""

import csv
from Simulations.run_monte import run_monte
from Loan.loan_pool import LoanPool
from Loan.auto_loan import AutoLoan
from Asset.cars import Car
from Tranche.structured_security import StructuredSecurity
from Timer.timer import Timer
from waterfall import do_waterfall

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
    # initialize loan pool
    with open('Loans_csv.csv') as file:
        reader = csv.DictReader(file)
        for row in reader:  # create loan objects
            loan = create_loan(row.get('Loan Type'), row.get('Asset'), row.get('Asset Value'), row.get('Balance'),
                               row.get('Rate'), row.get('Term'))
            loan_pool.loans.append(loan)  # add loan to loan pool

    # initialize structured security with tranches
    security = StructuredSecurity(loan_pool.total_principal(), 'Sequential')
    security.add_tranche(0.8, 0.05, 'A')
    security.add_tranche(0.2, 0.08, 'B')

    # waterfall function to get waterfall
    assets, liabilities, metrics = do_waterfall(loan_pool, security)
    print(metrics)
    newlist = []
    for x in liabilities:
        n = [item for sublist in x for item in sublist]
        newlist.append(n)

    with open('wf_liab_LOANS_SEQ_recoveries.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        header = ['Period',
                  'Interest Due A', 'Interest Paid A', 'Interest Shortfall A', 'Principal Paid A', 'Balance A',
                  'Interest Due B', 'Interest Paid B', 'Interest Shortfall B', 'Principal Paid B', 'Balance B',
                  'Reserve Account']  # header creation is not ideal.
        writer.writerow(header)
        writer.writerows(newlist)

    with open('wf_assets_LOANS_SEQ_recoveries.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        header = ['Period', 'Principal Due', 'Interest Due', 'Total', 'Recoveries', 'Balance']
        writer.writerow(header)
        writer.writerows(assets)

    # run monte function with parallel simulations
    with Timer('Timer final') as t:
        dirrs, als, tranche_ratings, irrs = run_monte(loan_pool, security, 0.005, 2000, 40)
        print(dirrs)
        print(als)
        print(tranche_ratings)
        print(irrs)


if __name__ == '__main__':
    main()
