#!/usr/bin/env python3
import fcntl
import sys
import subprocess
import os
import re
import multiprocessing
import math
import signal
import mmap
from threading import Timer
import time

import test.misc as misc
import test.globals as g

from time import sleep
def signal_handler(signal, frame):
    print('\n    [TERMINATED]')

signal.signal(signal.SIGINT, signal_handler)


term = sys.stdout

class Bdd:
    def __init__(this):
        this.compile_result = []
        this.inference_result = []
        this.repeat = 3
        this.partitions = 4
        this.compiler  = os.path.join(g.WMC_DIR,"bin/bnc")
        this.inference = os.path.join(g.WMC_DIR,"bin/bnmc")
        this.encoder   = os.path.join(g.WMC_DIR,"bin/bn-to-cnf")
        this.timeout = None
        this.dir = os.path.join(g.SCRIPT_DIR,"output")
        if not os.path.exists(this.dir):
            os.makedirs(this.dir)

    def set_partitions(partitions):
        this.partitions = partitions

    def set_bayesian_network(this,hugin):
        if not os.path.exists(hugin):
            nhugin = os.path.join(g.NET_DIR,"{}.net".format(net))
            if not os.path.exists(nhugin):
                sys.stderr.write("Bayesian network '{hugin}' not found".format(hugin))
                sys.exit(1)
            else:
                hugin = nhugin

        misc.require(hugin)
        this.hugin   = hugin
        this.net     = os.path.basename(hugin_ne)
        this.part    = this.dir + "/" + this.net + ".part"
        this.num     = this.dir + "/" + this.net + ".num"
        this.comp    = this.dir + "/" + this.net + ".comp"
        this.circuit = this.dir + "/" + this.net + ".ac"
        this.map     = this.dir + "/" + this.net + ".map"
        this.inf     = this.dir + "/" + this.net + ".inf"
        this.part_circuit = this.dir + "/" + this.net + ".0.ac"

    def clean(this):
        files = [ this.part, this.num, this.comp, this.circuit, this.map, this.inf, this.part_ciruit]
        for f in files:
            if os.path.exists(f):
                os.remove(f)

    def set_timeout(this, timeout):
        this.timeout = timeout

    def create_inference_input(this,bdds):
        print("load net {:s}\nload map {:s}\nload pwpbdd {:s} {:s} {:s}\ncompare".format(
            this.hugin,
            this.map,
            this.part_circuit,
            this.part,
            this.comp), file=open(this.inf, "w"))

    def compile(this,name,cmd):
        regex_seconds=r"Total time[: ]+([0-9.]+)s"
        regex_milliseconds=r"Total time[: ]+([0-9.]+)ms"
        regex_operators=r"Total #oper[a-z :]+([0-9]+)"

        this.compile_result.append([name,[],[],0])
        for i in range(this.repeat):
            matches = this.execute_find(cmd, None, [regex_seconds, regex_milliseconds, regex_operators])

            if matches[0] != None:
                this.compile_result[-1][1].append(float(matches[0].group(1)))
            if matches[1] != None:
                this.compile_result[-1][2].append(float(matches[1].group(1)))
            if matches[2] != None:
                this.compile_result[-1][3] = int(matches[2].group(1))

    def print_inference_results(this):
        misc.header("\n* Inference results ({})".format(this.net))
        if len(this.inference_result) == 0:
            print("Inference table is empty")
            return

        header = "\n{:>3} | {:>6s} | {:>12s} | {:>12s} | {:>12}\n".format("nr","cores","queries","seconds","speed-down")
        hline  = "-"*4 + "|-" + "-"*7 + "|-" + "-"*13 + "|-" + "-"*13 + "|-" + "-"*13 + "\n"
        term.write(header)
        term.write(hline)

        keys = []
        for i in range(len(this.inference_result)):
            keys.append((this.inference_result[i][2],i))
        keys = sorted(keys)

        row = "{:3d} | {:6d} | {:12d} | {:12.4f} | {:12.2f}\n"
        base_key = keys[0][1]
        for i in range(len(this.inference_result)):
            key = keys[i][1]
            term.write(row.format(
                i,
                this.inference_result[key][1],
                this.inference_result[key][0],
                this.inference_result[key][2],
                this.inference_result[key][2]/this.inference_result[base_key][2]))

    def print_compilation_results(this):
        misc.header("\n* Compilation results ({})".format(this.net))
        header = "\n{:3s} | {:34s} | {:>12s} | {:>12s} | {:>12s}\n"
        hline  = "-"*4 + "|-" + "-"*35 + "|-" + "-"*13 + "|-" + "-"*13 + "|-" + "-"*13 + "\n"
        term.write(header.format("nr","type","seconds","milliseconds","size"))
        term.write(hline)

        keys = []
        for i in range(len(this.compile_result)):
            avg_milliseconds = sum(this.compile_result[i][2]) / float(len(this.compile_result[i][2]))
            keys.append((avg_milliseconds,i))

        keys = sorted(keys)

        row = "{:3d} | {:34s}" + " | " + "{:12.3f}" + " | " + "{:12.3f}" + " | " + "{:12d}" + "\n"
        for i in range(len(this.compile_result)):
            key = keys[i][1]
            avg_seconds = sum(this.compile_result[key][1]) / float(len(this.compile_result[key][1]))
            avg_milliseconds = sum(this.compile_result[key][2]) / float(len(this.compile_result[key][2]))
            term.write(row.format(
                i,
                this.compile_result[key][0],
                avg_seconds,
                avg_milliseconds,
                this.compile_result[key][3]))

    def create_ordering(this,overwrite):
        misc.header("\n* Create ordering")
        if overwrite or not os.path.exists(this.num):
            cmd = "{:s} {:s} -o ordering_only=1 -w elim={:s}".format(this.compiler,this.hugin,this.num)
            this.call(cmd)
        else:
            term.write("    [SKIPPED]  \n")

    def create_partitioning(this,overwrite):
        misc.header("\n* Create partitioning")
        misc.require(this.num)
        if overwrite or not os.path.exists(this.part):
            cmd = "{:s} {:s} -o ordering_only=1 -r elim={:s} -o partitions={:d} -w part={:s}".format(this.compiler,this.hugin,this.num,this.partitions,this.part)
            this.call(cmd)
        else:
            term.write("    [SKIPPED]  \n")

    def create_composition_ordering(this,overwrite):
        misc.header("\n* Create componsition ordering")
        misc.require(this.num)
        misc.require(this.part)
        if overwrite or not os.path.exists(this.comp):
            cmd = "{:s} {:s} -o ordering_only=1 -r elim={:s} -r part={:s} -w comp={:s}".format(this.compiler,this.hugin,this.num,this.part,this.comp)
            this.call(cmd)
        else:
            term.write("    [SKIPPED]  \n")

    def create_circuit(this,overwrite):
        misc.header("\n* Create circuit")
        misc.require(this.num)
        if overwrite or not os.path.exists(this.circuit):
            cmd = "{:s} {:s} -r elim={:s} -w map={:s} -w circuit={:s}".format(this.compiler,this.hugin,this.num,this.map,this.circuit)
            this.call(cmd)
        else:
            term.write("    [SKIPPED]  \n")

    def create_partitioned_circuit(this,overwrite):
        misc.header("\n* Create partitioned circuit")
        misc.require(this.num)
        misc.require(this.part)
        if overwrite or not os.path.exists(this.part_circuit):
            cmd = "{:s} {:s} -r part={:s} -w map={:s} -w circuit={:s}".format(this.compiler,this.hugin,this.part,this.map,this.circuit)
            this.call(cmd)
        else:
            term.write("    [SKIPPED]  \n")

