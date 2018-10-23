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
import traceback
import test.misc as misc
import test.globals as g

from time import sleep
def signal_handler(signal, frame):
    print('\n    [TERMINATED]')

signal.signal(signal.SIGINT, signal_handler)

term = sys.stdout

MAX_CORES = multiprocessing.cpu_count()
CORES = [2**exp for exp in range(0,10) if 2**exp <= MAX_CORES]

class Bdd:
    def __init__(this):
        this.compile_result = []
        this.inference_result = []
        this.repeat = 3
        this.partitions = 2
        this.cores = CORES
        this.overwrite = False
        this.verify = False
        this.verbose = False
        this.ace       = os.path.join(g.WMC_DIR,"usr/bin/ace")
        this.compiler  = os.path.join(g.WMC_DIR,"bin/bnc")
        this.inference = os.path.join(g.WMC_DIR,"bin/bnmc")
        this.encoder   = os.path.join(g.WMC_DIR,"bin/bn-to-cnf")
        this.timeout = None
        this.dir = os.path.join(g.SCRIPT_DIR,"output")
        if not os.path.exists(this.dir):
            os.makedirs(this.dir)

    def set_verbose(this,verbose):
        this.verbose = verbose

    def set_repeat(this,repeat):
        this.repeat = repeat

    def set_verify(this,verify):
        this.verify = verify

    def set_overwrite(this,overwrite):
        this.overwrite = overwrite

    def set_ratio(this,ratio):
        this.ratio = ratio

    def set_partitions(this,partitions):
        this.partitions = partitions

    def set_cores(this,cores):
        this.cores = cores

    def get_partition_count():
        try:
            f = open(this.part, 'rb')
            f_gen = _make_gen(f.raw.read)
            return sum( buf.count(b'\n') for buf in f_gen )
        except:
            return 0

    def set_bayesian_network(this,hugin):
        if not os.path.exists(hugin):
            net,ext = os.path.splitext(hugin)
            net = os.path.basename(net)
            nhugin = os.path.join(g.NET_DIR,"{}.net".format(net))
            if not os.path.exists(nhugin):
                sys.stderr.write("Bayesian network '{}' not found".format(hugin))
                sys.exit(1)
            else:
                hugin = nhugin

        misc.require(hugin)
        this.hugin   = hugin
        this.net     = net
        this.part    = this.dir + "/" + this.net + ".part"
        this.num     = this.dir + "/" + this.net + ".num"
        this.part_num = this.dir + "/" + this.net + ".0.num"
        this.comp    = this.dir + "/" + this.net + ".comp"
        this.circuit = this.dir + "/" + this.net + ".ac"
        this.map     = this.dir + "/" + this.net + ".map"
        this.inf     = this.dir + "/" + this.net + ".inf"
        this.inference_out      = this.dir + "/" + this.net + ".inf.out"
        this.compilation_out    = this.dir + "/" + this.net + ".comp.out"
        this.part_circuit       = this.dir + "/" + this.net + ".0.ac"
        this.multigraph_circuit = this.dir + "/" + this.net + ".mc.ac"
        this.tdmultigraph_circuit = this.dir + "/" + this.net + ".tdmc.ac"

    def clean(this):
        files = [ this.part, this.num, this.comp, this.circuit, this.map, this.inf, this.part_ciruit, this.multigraph_circuit]
        for f in files:
            if os.path.exists(f):
                os.remove(f)

    def set_timeout(this, timeout):
        this.timeout = timeout

    def create_inference_input(this,bdds):
        f = open(this.inf, "w")
        f.write("load net {:s}\n".format(this.hugin))
        f.write("load map {:s}\n".format(this.map))
        if 'wpbdd' in bdds:
            f.write("load wpbdd {:s}\n".format(this.circuit))
        if 'pwpbdd' in bdds or 'parallel-pwpbdd' in bdds:
            f.write("load pwpbdd {:s} {:s} {:s}\n".format(this.part_circuit,this.part,this.comp))
        if 'tdmg' in bdds:
            f.write("load tdmg {:s}\n".format(this.tdmultigraph_circuit))
        if 'mg' in bdds:
            f.write("load mg {:s}\n".format(this.multigraph_circuit))
        if 'dlib' in bdds:
            f.write("initdlib\n");
        if 'ace' in bdds:
            f.write("ace\n");

        if this.verify:
            f.write("verify\n");
        else:
            f.write("compare 1\n")
        f.close()

    def compile(this,name,cmd):
        regex_seconds=r"Total time[: ]+([0-9.]+)s"
        regex_milliseconds=r"Total time[: ]+([0-9.]+)ms"
        regex_operators=r"Total #oper[a-z :]+([0-9]+)"
        regex_nodes=r"Total #nodes[ :]+([0-9]+)"
        regex_edges=r"Total #edges[ :]+([0-9]+)"

        this.compile_result.append([name,[],[],0,0,0])
        for i in range(this.repeat):
            if this.repeat > 1:
                misc.header("  - Run {} of {}".format(i+1,this.repeat))
            matches = misc.execute_find(cmd, None, [regex_seconds, regex_milliseconds, regex_operators,regex_nodes,regex_edges], this.timeout, this.verbose)

            if len(matches[0]) != 0:
                this.compile_result[-1][1].append(float(matches[0][0]))
            else:
                this.compile_result[-1][1].append(float('inf'))

            if len(matches[1]) != 0:
                this.compile_result[-1][2].append(float(matches[1][0]))
            else:
                this.compile_result[-1][2].append(float('inf'))

            if len(matches[2]) != 0:
                this.compile_result[-1][3] = int(matches[2][0])
            else:
                this.compile_result[-1][3] = -1

            if len(matches[3]) != 0:
                this.compile_result[-1][4] = int(matches[3][0])
            else:
                this.compile_result[-1][4] = -1


            if len(matches[4]) != 0:
                this.compile_result[-1][5] = int(matches[4][0])
            else:
                this.compile_result[-1][5] = -1

    def print_inference_results(this):
        misc.header("\n* Inference results ({})".format(this.net))
        if len(this.inference_result) == 0:
            print("Inference table is empty")
            return

        keys = []
        for i in range(len(this.inference_result)):
            keys.append((this.inference_result[i][2],i))
        keys = sorted(keys)

        header = "\n{:>3} | {:>12s} | {:>6s} | {:>12s} | {:>12s} | {:>12s} | {:>12}\n".format("nr","type","cores","queries","milliseconds","ms/q","speed-down")
        hline  = "-"*4 + "|-" + "-"*13 + "|-" + "-"*7 + "|-" + "-"*13 + "|-" + "-"*13 + "|-" + "-"*13 + "|-" + "-"*13 + "\n"

        f = open(this.inference_out, 'w')
        term.write(header)
        f.write(header)
        term.write(hline)
        f.write(hline)

        row = "{:3d} | {:12s} | {:6d} | {:12d} | {:12.4f} | {:12.4f} | {:12.2f}\n"
        base_key = keys[0][1]
        for i in range(len(this.inference_result)):
            key = keys[i][1]

            try:
                final = this.inference_result[key][2]/this.inference_result[base_key][2]
            except:
                final = float("nan")

            frow = row.format(
                i,
                this.inference_result[key][3],
                this.inference_result[key][1],
                this.inference_result[key][0],
                this.inference_result[key][2],
                float(this.inference_result[key][2])/int(this.inference_result[key][0]),
                final)

            term.write(frow)
            f.write(frow)

        f.close()
        term.write("\nResults written to '{}'\n".format(this.inference_out))

    def print_compilation_results(this):
        misc.header("\n* Compilation results ({})".format(this.net))
        if len(this.compile_result) == 0:
            print("Compilation table is empty")
            return

        header = "\n{:3s} | {:34s} | {:>12s} | {:>12s} | {:>12s} | {:>12s} | {:>12s} | {:>12s}\n"
        hline  = "-"*4 + "|-" + "-"*35 + "|-" + "-"*13 + "|-" + "-"*13 + "|-" + "-"*13 + "|-" + "-"*13 + "|-" + "-"*13 +"|-" + "-"*13 + "\n"
        f = open(this.compilation_out, 'w')
        term.write(header.format("nr","type","seconds","milliseconds","speed-down","operators","nodes","edges"))
        f.write(header.format("nr","type","seconds","milliseconds","speed-down","operators","nodes","edges"))
        term.write(hline)
        f.write(hline)

        keys = []
        for i in range(len(this.compile_result)):
            try:
                avg_milliseconds = sum(this.compile_result[i][2]) / float(len(this.compile_result[i][2]))
                keys.append((avg_milliseconds,i))
            except: pass

        keys = sorted(keys)

        row = "{:3d} | {:34s}" + " | " + "{:12.3f}" + " | " + "{:12.3f}" + " | " + "{:12.3f}" + " | " + "{:12d}"  + " | " + "{:12d}" + " | " + "{:12d}" + "\n"
        avg_milliseconds_fast = -1
        for i in range(len(keys)):
            key = keys[i][1]
            avg_seconds = sum(this.compile_result[key][1]) / float(len(this.compile_result[key][1]))
            avg_milliseconds = sum(this.compile_result[key][2]) / float(len(this.compile_result[key][2]))
            if avg_milliseconds_fast == -1:
                avg_milliseconds_fast = float(avg_milliseconds)

            frow = row.format(
                i,
                this.compile_result[key][0],
                avg_seconds,
                avg_milliseconds,
                avg_milliseconds/avg_milliseconds_fast,
                this.compile_result[key][3],
                this.compile_result[key][4],
                this.compile_result[key][5])
            term.write(frow)
            f.write(frow)

        f.close()
        term.write("\nResults written to '{}'\n".format(this.compilation_out))

    def create_ordering(this):
        misc.header("\n* Create ordering")
        if this.overwrite or not os.path.exists(this.num):
            cmd = "{:s} {:s} -t wpbdd -o no_compile=1 -w elim={:s}".format(this.compiler,this.hugin,this.num)
            misc.call(cmd,this.verbose)
        else:
            term.write("    [SKIPPED]  \n")

    def create_partition_ordering(this):
        misc.header("\n* Create partition ordering")
        if this.overwrite or not os.path.exists(this.part_num):
            cmd = "{:s} {:s} -t wpbdd -o no_compile=1 -r part={:s} -w elim={:s}".format(this.compiler,this.hugin,this.part,this.num)
            misc.call(cmd,this.verbose)
        else:
            term.write("    [SKIPPED]  \n")

    def create_partitioning(this):
        misc.header("\n* Create partitioning")
        if this.overwrite or not os.path.exists(this.part):
            ratio = ""
            if float(this.ratio) != 2.0:
                ratio = "-o sa_score_ratio={:.2f}".format(this.ratio)

            cmd = "{:s} {:s} -t wpbdd -o no_compile=1 -o no_ordering=1 -o partitions={:d} -w part={:s} {:s}".format(this.compiler,this.hugin,this.partitions,this.part,ratio)
            misc.call(cmd,this.verbose)
        else:
            term.write("    [SKIPPED]  \n")

    def create_composition_ordering(this,):
        misc.header("\n* Create componsition ordering")
        misc.require(this.part)
        if this.overwrite or not os.path.exists(this.comp):
            cmd = "{:s} {:s} -t wpbdd -o no_compile=1 -o no_ordering=1 -r part={:s} -w comp={:s}".format(this.compiler,this.hugin,this.part,this.comp)
            misc.call(cmd,this.verbose)
        else:
            term.write("    [SKIPPED]  \n")

    def create_circuit(this):
        misc.header("\n* Create circuit")
        misc.require(this.num)
        if this.overwrite or not os.path.exists(this.circuit):
            cmd = "{:s} {:s} -t wpbdd -r elim={:s} -w map={:s} -w circuit={:s} -o collapse=0".format(this.compiler,this.hugin,this.num,this.map,this.circuit)
            misc.call(cmd,this.verbose)
        else:
            term.write("    [SKIPPED]  \n")

    def create_partitioned_circuit(this):
        misc.header("\n* Create partitioned circuit")
        misc.require(this.part_num)
        misc.require(this.part)
        if this.overwrite or not os.path.exists(this.part_circuit):
            cmd = "{:s} {:s} -t wpbdd -r part={:s} -r elim={:s} -w map={:s} -w circuit={:s} -o collapse=0".format(this.compiler,this.hugin,this.part,this.num,this.map,this.circuit)
            misc.call(cmd,this.verbose)
        else:
            term.write("    [SKIPPED]  \n")

    def create_tdmultigraph_circuit(this):
        misc.header("\n* Create tdmultigraph circuit")
        if this.overwrite or not os.path.exists(this.tdmultigraph_circuit):
            cmd = "{:s} {:s} -w map={:s} -w circuit={:s} -t tdmg".format(this.compiler,this.hugin,this.map,this.tdmultigraph_circuit)
            misc.call(cmd,this.verbose)
        else:
            term.write("    [SKIPPED]  \n")


    def create_multigraph_circuit(this):
        misc.header("\n* Create multigraph circuit")
        misc.require(this.num)
        if this.overwrite or not os.path.exists(this.multigraph_circuit):
            cmd = "{:s} {:s} -r elim={:s} -w map={:s} -w circuit={:s} -t mg".format(this.compiler,this.hugin,this.num,this.map,this.multigraph_circuit)
            misc.call(cmd,this.verbose)
        else:
            term.write("    [SKIPPED]  \n")

    def run_inference(this,bdds):
        allowed = set(['tdmg','mg','wpbdd','parallel-pwpbdd','pwpbdd','dlib','ace'])
        if not set(bdds).issubset(allowed):
            print("Bdd(s) not supported for inference: ",set(bdds)-allowed)
            sys.exit(1)

        if 'pwpbdd' in bdds or 'parallel-pwpbdd' in bdds or 'pmg' in bdds or 'ptdmg' in bdds:
            this.create_partitioning()
            this.create_partition_ordering()

        if 'wpbdd' in bdds or 'mg' in bdds or 'tdmg' in bdds:
            this.create_ordering()

        if 'wpbdd' in bdds:
            this.create_circuit()
        if 'mg' in bdds:
            this.create_multigraph_circuit()
        if 'tdmg' in bdds:
            this.create_tdmultigraph_circuit()
        if 'pwpbdd' in bdds or 'parallel-pwpbdd' in bdds or 'pmg' in bdds or 'ptdmg' in bdds:
            this.create_partitioned_circuit()
            this.create_composition_ordering()

        this.create_inference_input(bdds)
        misc.require(this.inf)

        if 'parallel-pwpbdd' in bdds:
            cores_arg = []
            for cores in this.cores:
                cores_arg += ['-w','{}'.format(cores)]
            cmd = [this.inference] + cores_arg
        else:
            cmd = [this.inference]

        regex_query=r"Query[ ]+[0-9]+[( ]+([0-9]+)\)"
        regex_time = []
        regex_time.append(r"([a-zA-Z][^\ ]*)[ ]+\(([.0-9]+)\)")

        misc.header("\n* Run Inference")
        matches = misc.execute_find(cmd, this.inf, [regex_query] + regex_time, this.timeout, this.verbose)
        result = []
        queries = 0
        if len(matches[0]) != 0:
            queries = int(matches[0][0])

            # wpbdd
            key = 1
            for match in matches[key]:
                algorithm = match[0]
                time = float(match[1])
                this.inference_result.append([queries,1,time,algorithm])



    def help_encoding(this):
        cmd = "{:s} -h".format(this.encoder)
        misc.call(cmd,True)

    def run_encoding(this,args):
        if args == None:
            cmd = "{:s} -i {:s} -s".format(this.encoder,this.hugin)
        else:
            cmd = "{:s} -i {:s} -s {:s}".format(this.encoder,this.hugin," ".join(args))
        misc.call(cmd,True)

    def run_compilation(this,bdds):
        this.create_ordering()
        if 'pwpbdd' in bdds or 'parallel-pwpbdd' in bdds:
            this.create_partitioning()
        misc.require(this.num)

        if 'mg' in bdds:
            misc.header("\n* Compile MULTIGRAPH")
            cmd = [this.compiler,this.hugin,"-r","elim={:s}".format(this.num),"-t","mg"]
            this.compile("MG",cmd)

        if 'tdmg' in bdds:
            misc.header("\n* Compile TDMULTIGRAPH")
            cmd = [this.compiler,this.hugin,"-t","tdmg"]
            this.compile("TDMG",cmd)

        if 'wpbdd' in bdds:
            misc.header("\n* Compile WPBDD")
            cmd = [this.compiler,this.hugin,"-r","elim={:s}".format(this.num),"-t","wpbdd"]
            this.compile("WPBDD",cmd)

        if 'pwpbdd' in bdds:
            misc.require(this.part)
            misc.header("\n* Compile partitioned WPBDD")
            cmd = [this.compiler,this.hugin,"-r","part={:s}".format(this.part),"-t","wpbdd","-d","partitioned"]
            this.compile("PWPBDD",cmd)

        if 'ace' in bdds:
            misc.header("\n* Compile d-DNNF")
            cmd = [this.ace,"--network","{}".format(this.hugin),"--compile"]
            this.compile("ACE",cmd)

        if 'acei' in bdds:
            misc.header("\n* Compile d-DNNF")
            cmd = [this.ace,"--network","{}".format(this.hugin),"--compile","--with-init"]
            this.compile("ACEI",cmd)

        if 'obdd' in bdds:
            misc.header("\n* Compile OBDD (CUDD)")
            cmd = [this.compiler,this.hugin,"-r","elim={:s}".format(this.num),"-t","obdd","-o","determinism=0"]
            this.compile("OBDD (CUDD)",cmd)

        if 'zbdd' in bdds:
            misc.header("\n* Compile ZBDD (CUDD)")
            cmd = [this.compiler,this.hugin,"-r","elim={:s}".format(this.num),"-t","zbdd","-o","determinism=0"]
            this.compile("ZBDD (CUDD)",cmd)

        if 'sddr' in bdds:
            misc.header("\n* Compile right aligned vtree SDD (SDD compiler)")
            cmd = [this.compiler,this.hugin,"-r","elim={:s}".format(this.num),"-t","sddr","-o","determinism=0"]
            this.compile("rSDD (SDD compiler)",cmd)

        if 'sdd' in bdds:
            misc.header("\n* Compile balanced vtree SDD (SDD compiler)")
            cmd = [this.compiler,this.hugin,"-r","elim={:s}".format(this.num),"-t","sdd","-o","determinism=0"]
            this.compile("SDD (SDD compiler)",cmd)

        if 'parallel-wpbdd' in bdds or 'parallel-pwpbdd' in bdds:
            for cores in this.cores:
                if 'parallel-wpbdd' in bdds:
                    misc.header("\n* Compile WPBDD - sylvan {:d} core(s)".format(cores))
                    cmd = [this.compiler,this.hugin,"-t","sylvan","-o","determinism=0","-r","elim={:s}".format(this.num),"-o","workers={:d}".format(cores)]
                    this.compile("parallel WPBDD {:d} core(s)".format(cores),cmd)

                if 'parallel-pwpbdd' in bdds:
                    misc.require(this.part)
                    misc.header("\n* Compile partitioned WPBDD - silvan {:d} core(s)".format(cores))
                    cmd = [this.compiler,this.hugin,"-d","partitioned","-t","sylvan","-o","determinism=0","-p","-r","part={:s}".format(this.part),"-o","workers={:d}".format(cores)]
                    this.compile("Parallel PWPBDD {:d} core(s)".format(cores),cmd)

                    misc.header("\n* Compile partitioned PWPBDD - silvan (+1) {:d} core(s)".format(cores))
                    cmd = [this.compiler,this.hugin,"-d","partitioned","-t","sylvan","-o","determinism=0","-p","-r","part={:s}".format(this.part),"-o","workers={:d}".format(cores),"-o","parallel_partition=1","-o","parallel_conjoin=0","-o","parallel_cpt=0" ]
                    this.compile("Parallel PWPBDD +1opt {:d} core(s)".format(cores),cmd)

                    misc.header("\n* Compile partitioned PWPBDD - silvan (+2) {:d} core(s)".format(cores))
                    cmd = [this.compiler,this.hugin,"-d","partitioned","-t","sylvan","-o","determinism=0","-p","-r","part={:s}".format(this.part),"-o","workers={:d}".format(cores),"-o","parallel_partition=1","-o","parallel_conjoin=1","-o","parallel_cpt=0" ]
                    this.compile("Parallel PWPBDD +2opt {:d} core(s)".format(cores),cmd)

                    misc.header("\n* Compile partitioned PWPBDD - silvan (+3 opt) {:d} core(s)".format(cores))
                    cmd = [this.compiler,this.hugin,"-d","partitioned","-t","sylvan","-o","determinism=0","-p","-r","part={:s}".format(this.part),"-o","workers={:d}".format(cores),"-o","parallel_partition=1","-o","parallel_conjoin=1","-o","parallel_cpt=1" ]
                    this.compile("Parallel PWPBDD +3opt {:d} core(s)".format(cores),cmd)


