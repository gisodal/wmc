#!/usr/bin/env python3

import test.misc as misc
import test.globals as g
from test.bdd import *

def compare_inference(options):
    for network in options.networks:
        bdd = Bdd()
        bdd.set_cores(options.cores)
        bdd.set_overwrite(options.overwrite)
        bdd.set_verify(options.verify)
        bdd.set_bayesian_network(network)
        bdd.set_partitions(options.partitions)
        bdd.set_verbose(options.verbose)
        #bdd.set_timeout(5)
        bdd.run_inference(options.bdds)
        #bdd.set_timeout(None)
        bdd.print_inference_results()


def compare_compilation(options):
    for network in options.networks:
        bdd = Bdd()
        bdd.set_cores(options.cores)
        bdd.set_overwrite(options.overwrite)
        bdd.set_bayesian_network(network)
        bdd.set_repeat(options.repeat);
        bdd.set_verbose(options.verbose)
        bdd.set_partitions(options.partitions)
        bdd.run_compilation(options.bdds)
        bdd.print_compilation_results()

def compare_encoding(options):
    if options.help:
        bdd = Bdd()
        bdd.help_encoding()
    else:
        for network in options.networks:
            bdd = Bdd()
            bdd.set_bayesian_network(network)
            bdd.set_verbose(options.verbose)
            bdd.run_encoding(options.args)

