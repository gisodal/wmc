#!/usr/bin/env python3

import test.misc as misc
import test.globals as g
from test.bdd import *

def compare_inference(bdds,networks,partitions,overwrite):
    for network in networks:
        bdd = Bdd()
        bdd.set_overwrite(overwrite)
        bdd.set_bayesian_network(network)
        bdd.set_partitions(partitions)
        bdd.set_timeout(5)
        bdd.run_inference(bdds)
        bdd.set_timeout(None)
        bdd.print_inference_results()


def compare_compilation(bdds,networks,partitions,overwrite):
    for network in networks:
        bdd = Bdd()
        bdd.set_overwrite(overwrite)
        bdd.set_bayesian_network(network)
        bdd.set_partitions(partitions)
        bdd.run_compilation(bdds)
        bdd.print_compilation_results()


