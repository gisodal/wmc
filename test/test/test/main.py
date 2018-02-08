#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import sys
import test.misc as misc
import .bdd

def main(argv):
    parser = argparse.ArgumentParser(description='WMC testing suite')

    test_options = ["compilation","inference","encoding"]
    parser.add_argument('-t','--test',nargs=1,choices=test_options, help='Choose what to test', required=False)

    #dataset_options = ["ijcai"]
    #parser.add_argument('-d','--dataset',nargs=1,choices=dataset_options, help='Dataset used for testing', required=False, default='ijcai')

    bdd_options = ["wpbdd","pwpbdd","sdd","obdd"]
    parser.add_argument('-b','--bdd',nargs=1, help='Type of BDD', required=False,default=bdd_options[0])
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-n','--network',nargs=1, help='Bayesian network used for testing')
    group.add_argument('-h','--hugin',nargs=1, help='Hugin file used for testing')
    parser.add_argument('-l','--list', action='store_true', help='List of available Bayesian networks', required=False)

    args = vars(parser.parse_args())

    print(args)
    if args['list'] == True:
        misc.list_bayesian_networks()
    else:

        bdd = Bdd()
        if 'hugin' in args:
            bdd.set_hugin_network(args['hugin'])
        elif 'network' in args:
            bdd.set_bayesian_network(args['network'])

        overwrite = False
        bdd.create_ordering(overwrite)
        bdd.create_partitioning(overwrite)
        bdd.create_circuit(overwrite)
        bdd.create_partitioned_circuit(overwrite)

        bdd.compare_compilation()

        bdd.create_composition_ordering(overwrite)
        bdd.set_timeout(5)
        bdd.compare_inference()
        bdd.set_timeout(None)

        bdd.print_compilation_results()
        bdd.print_inference_results()





if __name__ == "__main__":
   main(sys.argv[1:])

