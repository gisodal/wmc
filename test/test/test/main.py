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
                inference(options)
            elif options.test == "compilation":
                compare_compilation(options.bdds,options.networks,options.partitions,options.overwrite)
            else:
                pass



def main():
    parser = argparse.ArgumentParser(description='WMC testing suite',add_help=False)

    parser.add_argument('--help',action='help',help='Show this help message and exit')

    test_options = ["compilation","inference","encoding"]
    parser.add_argument('--test',dest='test',choices=test_options, help='Choose what to test. Choices are ' + ', '.join(test_options), required=False,metavar='TEST')

    bdd_options = ["wpbdd","parallel-wpbdd","pwpbdd","parallel-pwpbdd","sdd","sddr","obdd","zbdd"]
    parser.add_argument('--bdd',dest='bdds',nargs='+', help='Type of BDD. Choices are ' + ', '.join(bdd_options), choices=bdd_options,required=False,default=None,metavar='BDD')
    parser.add_argument('--network',dest='networks',nargs='+', help='Bayesian network(s) used for testing')
    parser.add_argument('--partitions',dest='partitions',help='Set number of partitions',default=2,type=int)
    parser.add_argument('--overwrite',dest='overwrite',action='store_true', help='Overwrite ordering, partitioning, etc.')
    parser.add_argument('--list', dest='list', action='store_true', help='Print list of available Bayesian networks', required=False)

    if len(sys.argv)==1:
        parser.print_help()
        sys.exit(0)

    options = parser.parse_args()
    process(options)

if __name__ == "__main__":
   main(sys.argv[1:])

