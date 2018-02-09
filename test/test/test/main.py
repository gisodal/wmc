#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import sys
from test.misc import *
from test.bdd import *
from test.experiments import *

def main(argv):
    parser = argparse.ArgumentParser(description='WMC testing suite',add_help=False)

    parser.add_argument('--help',action='help',help='Show this help message and exit')

    group = parser.add_mutually_exclusive_group(required=False)
    test_options = ["compilation","inference","encoding"]
    group.add_argument('--test',dest='test',nargs=1,choices=test_options, help='Choose what to test. Choices are ' + ', '.join(test_options), required=False,metavar='TEST')
    exp_options = ["compilation","inference"]
    group.add_argument('--experiment',dest='experiment',nargs=1,choices=test_options, help='Choose an experiment. Choices are ' + ', '.join(exp_options), required=False,metavar='EXP')

    #dataset_options = ["ijcai"]
    #parser.add_argument('-d','--dataset',nargs=1,choices=dataset_options, help='Dataset used for testing', required=False, default='ijcai')

    bdd_options = ["wpbdd","pwpbdd","parallel-pwpbdd","sdd","rsdd","obdd"]
    parser.add_argument('--bdd',dest='bdd',nargs='+', help='Type of BDD. Choices are ' + ', '.join(bdd_options), choices=bdd_options, required=False,default=None,metavar='BDD')
    group = parser.add_mutually_exclusive_group(required=False)
    group.add_argument('--network',dest='network',nargs='+', help='Bayesian network used for testing')
    group.add_argument('--hugin', dest='hugin',nargs='+', help='Path of Hugin file used for testing')
    parser.add_argument('--list', dest='list', action='store_true', help='Print list of available Bayesian networks', required=False)

    if len(sys.argv)==1:
        parser.print_help()
        sys.exit(0)

    options = parser.parse_args()

    if options.list == True:
        list_bayesian_networks()
        sys.exit(0)
    else:

        bdd = Bdd()
        #if 'hugin' in args:
        #    bdd.set_hugin_network(args['hugin'])
        #elif 'network' in args:
        #    bdd.set_bayesian_network(args['network'])

        #overwrite = False
        #bdd.create_ordering(overwrite)
        #bdd.create_partitioning(overwrite)
        #bdd.create_circuit(overwrite)
        #bdd.create_partitioned_circuit(overwrite)

        #bdd.compare_compilation()

        #bdd.create_composition_ordering(overwrite)
        #bdd.set_timeout(5)
        #bdd.compare_inference()
        #bdd.set_timeout(None)

        #bdd.print_compilation_results()
        #bdd.print_inference_results()





if __name__ == "__main__":
   main(sys.argv[1:])

