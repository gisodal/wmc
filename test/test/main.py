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
                compare_inference(options.bdds,options.networks,options.partitions,options.overwrite)
            elif options.test == "compilation":
                compare_compilation(options.bdds,options.networks,options.partitions,options.overwrite)
            else:
                compare_encoding(options.networks,options.help,options.args)


def main():
    parser = argparse.ArgumentParser(description='WMC testing suite',add_help=False)

    parser.add_argument('--help',action='help',help='Show this help message and exit')
    parser.add_argument('--list', dest='list', action='store_true', help='Print list of available Bayesian networks', required=False)
    test_options = ["compilation","inference","encoding"]
    parser.add_argument('--test',dest='test',choices=test_options, help='Choose what to test. Options are ' + ', '.join(test_options), required=False,metavar='TEST')
    parser.add_argument('--network',dest='networks',nargs='+', help='Bayesian network(s) used for testing',metavar="NETWORK")

    bdd_options = ["wpbdd","parallel-wpbdd","pwpbdd","parallel-pwpbdd","sdd","sddr","obdd","zbdd"]
    group = parser.add_argument_group('inference and compilation arguments')
    group.add_argument('--bdd',dest='bdds',nargs='+', help='Type of BDD. Options are ' + ', '.join(bdd_options), choices=bdd_options,required=False,default=None,metavar='BDD')
    group.add_argument('--partitions',dest='partitions',help='Set number of partitions',default=2,type=int,metavar='#PARTITIONS')
    group.add_argument('--overwrite',dest='overwrite',action='store_true', help='Overwrite ordering, partitioning, etc.')

    group = parser.add_argument_group('encoding arguments')
    group.add_argument('--encoding-help',dest='help',action='store_true',help='Show help for encoding')
    group.add_argument('--args',dest='args',nargs=argparse.REMAINDER,help="Encoding arguments",metavar='ARG')

    if len(sys.argv)==1:
        parser.print_help()
        sys.exit(0)

    options = parser.parse_args()

    if options.test == 'compilation' or options.test == 'inference':
        if options.networks == None or options.bdds == None:
            parser.error('{} requires --network and --bdd'.format(options.test))

    if options.test == 'encoding':
        if not options.help and (options.networks == None):
            parser.error('{} requires --network'.format(options.test))

    process(options)

if __name__ == "__main__":
   main(sys.argv[1:])

