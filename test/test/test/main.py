#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import sys
from test.misc import *
from test.bdd import *
from test.experiments import *

def process(options):
    if options.list == True:
        list_bayesian_networks()
        sys.exit(0)
    else:

        if options.test != None:
            if options.test == "inference":
                compare_inference(options)
            elif options.test == "compilation":
                compare_compilation(options)
            else:
                encoding(options)

def main():
    parser = argparse.ArgumentParser(description='WMC testing suite',add_help=False)

    parser.add_argument('--help',action='help',help='Show this help message and exit')

    group = parser.add_mutually_exclusive_group(required=False)
    test_options = ["compilation","inference","encoding"]
    group.add_argument('--test',dest='test',nargs=1,choices=test_options, help='Choose what to test. Choices are ' + ', '.join(test_options), required=False,metavar='TEST')

    #dataset_options = ["ijcai"]
    #parser.add_argument('-d','--dataset',nargs=1,choices=dataset_options, help='Dataset used for testing', required=False, default='ijcai')

    bdd_options = ["wpbdd","parallel-wpbdd","pwpbdd","parallel-pwpbdd","sdd","rsdd","obdd"]
    parser.add_argument('--bdd',dest='bdds',nargs='+', help='Type of decision diagram. Choices are ' + ', '.join(bdd_options), choices=bdd_options,required=False,default=None,metavar='BDD')
    group = parser.add_mutually_exclusive_group(required=False)
    parser.add_argument('--network',dest='network',nargs='+', help='Path(s) or basename(s) of HUGIN files')
    parser.add_argument('--list', dest='list', action='store_true', help='Print a list of available Bayesian networks', required=False)

    if len(sys.argv)==1:
        parser.print_help()
        sys.exit(0)

    options = parser.parse_args()
    print(options)
    process(options)

if __name__ == "__main__":
   main(sys.argv[1:])

