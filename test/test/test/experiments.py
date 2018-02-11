#!/usr/bin/env python3

import test.misc as misc
import test.globals as g
from test.bdd import *

#def compare_inference(options):
#    is_hugin = True
#    data = options.hugin
#    if len(options.hugin) == 0:
#        is_hugin = False
#        data = options.networks
#
#    for i in range(len(data)):
#        bdd = Bdd()
#        if is_hugin:
#            bdd.set_hugin_network(data[i])
#        else:
#            bdd.set_bayesian_network(data[i])
#
#        overwrite = False
#        bdd.create_ordering(overwrite)
#        bdd.create_circuit(overwrite)
#        if 'pwpbdd' in bdds or 'parallel-pwpbdds' in bdds:
#            bdd.create_partitioning(overwrite)
#            bdd.create_composition_ordering(overwrite)
#            bdd.create_partitioned_circuit(overwrite)
#
#        bdd.set_timeout(5)
#        bdd.compare_inference()
#        bdd.set_timeout(None)
#
#        bdd.print_inference_results()
#


def compare_inference(this,bdds):
        misc.header("\n* Compare inference")

        misc.require(this.map)
        misc.require(this.circuit)
        if 'pwpbdd' in bdds or 'parallel-pwpbdds' in bdds:
            misc.require(this.comp)
            misc.require(this.part)
            misc.require(this.part_circuit)

        this.create_inference_input(bdds)

        misc.require(this.inf)

        MAX_CORES = multiprocessing.cpu_count()
        CORES = [2**exp for exp in range(0,10) if 2**exp <= MAX_CORES]

        cmd = [this.inference]
        regex_query=r"Query[ ]+[0-9]+[( ]+([0-9]+)\)"
        regex_time = []
        for cores in CORES:
            regex_time.append(r"\)[ ]+PPWPBDD[0-9][- ]+({})[ ]+cores[ ]+\(([.0-9]+)\)".format(cores))

        matches = this.execute_find(cmd, this.inf, [regex_query] + regex_time)
        result = []
        queries = 0
        if matches[0] != None:
            queries = int(matches[0].group(1))

        key = 0
        for cores in CORES:
            key = key + 1
            if matches[key] != None: # 1 cores
                this.inference_result.append([queries,int(matches[key].group(1)),float(matches[key].group(2))])





def compare_compilation(bdds,networks,partitions,overwrite):

    for network in networks:
        bdd = Bdd()
        bdd.set_bayesian_network(network)
        bdd.set_partitions(partitions)
        bdd.create_ordering(overwrite)
        bdd.create_partitioning(overwrite)
        bdd.compilation(bdds)
        bdd.print_compilation_results()


