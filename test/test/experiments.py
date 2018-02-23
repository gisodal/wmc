#!/usr/bin/env python3

import test.misc as misc
import test.globals as g
from test.bdd import *

def compare_inference(bdds,networks,partitions,cores,overwrite):
    for network in networks:
        bdd = Bdd()
        bdd.set_cores(cores)
        bdd.set_overwrite(overwrite)
        bdd.set_bayesian_network(network)
        bdd.set_partitions(partitions)
        #bdd.set_timeout(5)
        bdd.run_inference(bdds)
        #bdd.set_timeout(None)
        bdd.print_inference_results()


def compare_compilation(bdds,networks,partitions,cores,overwrite):
    for network in networks:
        bdd = Bdd()
        bdd.set_cores(cores)
        bdd.set_overwrite(overwrite)
        bdd.set_bayesian_network(network)
        bdd.set_partitions(partitions)
        bdd.run_compilation(bdds)
        bdd.print_compilation_results()

def compare_encoding(networks,help_arg,args):
    if help_arg:
        bdd = Bdd()
        bdd.help_encoding()
    else:
        for network in networks:
            bdd = Bdd()
            bdd.set_bayesian_network(network)
            bdd.run_encoding(args)

