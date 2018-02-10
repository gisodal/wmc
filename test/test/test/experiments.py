#!/usr/bin/env python3

import test.misc as misc
import test.globals as g


def compare_inference(options):
    is_hugin = True
    data = options.hugin
    if len(options.hugin) == 0:
        is_hugin = False
        data = options.networks

    for i in range(len(data)):
        bdd = Bdd()
        if is_hugin:
            bdd.set_hugin_network(data[i])
        else:
            bdd.set_bayesian_network(data[i])

        overwrite = False
        bdd.create_ordering(overwrite)
        bdd.create_circuit(overwrite)
        if 'pwpbdd' in bdds or 'parallel-pwpbdds' in bdds:
            bdd.create_partitioning(overwrite)
            bdd.create_composition_ordering(overwrite)
            bdd.create_partitioned_circuit(overwrite)

        bdd.set_timeout(5)
        bdd.compare_inference()
        bdd.set_timeout(None)

        bdd.print_inference_results()



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





def compare_compilation(this):
        #misc.header("\n* Compile WPBDD")
        #cmd = [this.compiler,this.hugin,"-r","elim={:s}".format(this.num),"-o","collapse=0"]
        #this.compile("WPBDD",cmd)

        #misc.header("\n* Compile partitioned WPBDD")
        #cmd = [this.compiler,this.hugin,"-r","part={:s}".format(this.part),"-o","collapse=0"]
        #this.compile("PWPBDD",cmd)

        MAX_CORES = multiprocessing.cpu_count()
        CORES = [2**exp for exp in range(0,10) if 2**exp <= MAX_CORES]
        for cores in CORES:
            misc.header("\n* Compile WPBDD - sylvan {:d} core(s)".format(cores))
            cmd = [this.compiler,this.hugin,"-p","-r","elim={:s}".format(this.num),"-o","workers={:d}".format(cores)]
            this.compile("parallel WPBDD {:d} core(s)".format(cores),cmd)

            misc.header("\n* compile partitioned WPBDD - silvan {:d} core(s)".format(cores))
            cmd = [this.compiler,this.hugin,"-p","-r","part={:s}".format(this.part),"-o","workers={:d}".format(cores)]
            this.compile("Parallel PWPBDD {:d} core(s)".format(cores),cmd)

            misc.header("\n* Compile partitioned PWPBDD - silvan (+1) {:d} core(s)".format(cores))
            cmd = [this.compiler,this.hugin,"-p","-r","part={:s}".format(this.part),"-o","workers={:d}".format(cores),"-o","parallel_partition=1" ]
            this.compile("Parallel PWPBDD +1opt {:d} core(s)".format(cores),cmd)

            misc.header("\n* Compile partitioned PWPBDD - silvan (+2) {:d} core(s)".format(cores))
            cmd = [this.compiler,this.hugin,"-p","-r","part={:s}".format(this.part),"-o","workers={:d}".format(cores),"-o","parallel_partition=1","-o","parallel_conjoin=1" ]
            this.compile("Parallel PWPBDD +2opt {:d} core(s)".format(cores),cmd)

            misc.header("\n* Compile partitioned PWPBDD - silvan (+3 opt) {:d} core(s)".format(cores))
            cmd = [this.compiler,this.hugin,"-p","-r","part={:s}".format(this.part),"-o","workers={:d}".format(cores),"-o","parallel_partition=1","-o","parallel_conjoin=1","-o","parallel_cpt=1"]
            this.compile("Parallel PWPBDD +3opt {:d} core(s)".format(cores),cmd)

