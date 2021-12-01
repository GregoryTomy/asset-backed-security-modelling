"""This script contains the Monte Carlo function"""
from Simulations.sim_waterfall import simulate_waterfall
from Simulations.sim_waterfall_parallel import simulate_waterfall_parallel
import numpy as np


def run_monte(loanpool, structuredsecurity, tolerance, num_sim, num_processes):
    """Runs the Monte Carlo simulation"""
    old_rates = structuredsecurity.get_rates()
    tranche_notionals = structuredsecurity.get_notionals()
    tranche_coeffs = [1.2, 0.8]  # should be a property in tranche class but given here for now
    diff = tolerance * 2  # start of diff as greater than tolerance
    dirrs = None
    als = None
    irrs = None

    while diff > tolerance:
        # dirrs, als, irrs = simulate_waterfall(loanpool, structuredsecurity, num_sim)
        dirrs, als, irrs = simulate_waterfall_parallel(loanpool, structuredsecurity, num_sim, num_processes)
        yield_rates = [calculate_yield(d, a) for d, a in zip(dirrs, als)]
        new_rates = [new_tranche_rate(o, y, c) for o, y, c in zip(old_rates, yield_rates, tranche_coeffs)]
        diff = calculate_difference(old_rates, new_rates, tranche_notionals)
        old_rates = new_rates  # replace old rates with new rates for loop

    tranche_ratings = [get_rating(d) for d in dirrs]

    return [dirrs, als, tranche_ratings, irrs]


def calculate_yield(dirr, al):
    yield_rate = ((7 / (1 + .08 * np.exp(-0.19 * al / 12))) + 0.19 * np.sqrt(al / 12 * dirr * 100)) / 100
    return yield_rate


def new_tranche_rate(old_rate, yield_rate, coefficient):
    """Calculates new rate based on relaxation"""
    return old_rate + coefficient * (yield_rate - old_rate)


def calculate_difference(old_rates, new_rates, notionals):
    difference = [(old - new) / old for old, new in zip(old_rates, new_rates)]
    return np.average(difference, weights=notionals)


def get_rating(dirr):
    DIRR_bps = np.array([-np.inf, 0.06, 0.67, 1.3, 2.7, 5.2, 8.9, 13, 19,
                         27, 46, 72, 106, 143, 183, 231, 311, 2500, 10000])
    letter_ratings = ["Aaa", "Aa1", "Aa2", "Aa3", "A1", "A2", "A3", "Baa1", "Baa2",
                      "Baa3", "Ba1", "Ba2", "Ba3", "B1", "B2", "B3", "Caa", "Ca"]
    index = np.where(DIRR_bps >= dirr * 10000.0)[0][0] - 1
    return letter_ratings[index]
