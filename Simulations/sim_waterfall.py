"""This module contains the simulate waterfall function"""
from waterfall import do_waterfall
from statistics import mean
import numpy as np


def simulate_waterfall(loanpool, structuredsecurity, num_sim):
    dirr_sims = []
    al_sims = []
    irr_sims = []

    for i in range(num_sim):
        loanpool.reset()
        structuredsecurity.reset()
        _, _, metrics = do_waterfall(loanpool, structuredsecurity)
        metrics_transposed = np.array(metrics).T  # transpose metrics
        irr_sims.append(metrics_transposed[0])
        dirr_sims.append(metrics_transposed[1])
        al_sims.append(metrics_transposed[2])

    # calculate averages
    irr_average = np.mean(irr_sims, axis =0)
    dirr_average = np.mean(dirr_sims, axis=0)
    al_average = np.mean(al_sims, axis=0)
    return [dirr_average, al_average, irr_average]

    # tranch_subs = [tranche.subordination for tranche in structuredsecurity.tranches]
    #
    # for sub in tranch_subs:
    #     tranche_dirr[sub] = [res[sub] for res in dirr_sims]
    #     tranche_al[sub] = [res[sub] for res in al_sims]
    #
    # # convert to list comprehensions
    #
    # for sub, dirrs in tranche_dirr.items():
    #     dirr_averages[sub] = mean(dirrs)
    #
    # for sub, als in tranche_al.items():
    #     al_averages[sub] = mean([x for x in als if x is not None])
