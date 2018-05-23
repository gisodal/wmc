#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import fcntl
import subprocess
import glob
import os
import test.globals as g
import sys
from time import sleep
import re
term = sys.stdout
import traceback
import types
import signal

def print_list(lst):
    entries = len(lst)
    column_width = max(len(entry) for entry in lst)
    column_max = 5
    column_padding = 2
    column_format = "{:>" + str(column_width) + "}" + " "*column_padding

    row_width = int(os.popen('stty size', 'r').read().split()[1])
    columns = int(row_width/(column_width+column_padding))
    columns = min(max(1,min(column_max,columns)),entries)
    rows,remainder = divmod(entries, columns)
    if remainder > 0:
        rows = rows + 1

    for offset in range(rows):
        print("".join([column_format.format(entry) for entry in lst[offset::rows]]))


def list_bayesian_networks():
    bns_glob = glob.glob(os.path.join(g.NET_DIR,"*.net"), recursive=False)
    bns = [ os.path.splitext(os.path.basename(bn))[0] for bn in bns_glob ]
    bns = sorted(bns, key=str.lower)

    if len(bns) > 0:
        print_list(bns)
    else:
        print("No Bayesian networks found in '{}'".format(g.NET_DIR))

def execute_find(cmd, infile, expressions, timeout,verbose):
    if verbose:
        if infile == None:
            print(">"," ".join(cmd))
        else:
            print(">"," ".join(cmd), "<",infile)
    else:
        term.write("    [RUNNING]\r")

    # start cmd and pipe to tee
    try:
        if infile == None:
            input = None
        else:
            input = open(infile,'rb')

        fd_r, fd_w = os.pipe()
        command = subprocess.Popen(cmd,stdout=subprocess.PIPE,stdin=input)
        tee = subprocess.Popen(["tee", "/proc/{}/fd/{}".format(os.getpid(),fd_w)],
            stdin=command.stdout,stderr=subprocess.STDOUT)

        fl = fcntl.fcntl(fd_r, fcntl.F_GETFL)
        fcntl.fcntl(fd_r, fcntl.F_SETFL, fl | os.O_NONBLOCK)
        output = os.fdopen(fd_r)

        matches = [ [] ] * len(expressions)
        start = time.time()
        timedout = False
        while tee.poll() is None:
            sleep(0.001)
            if timeout is not None and time.time() - start >= timeout:
                timedout = True
                command.kill()

            while True:
                line = output.readline()
                if line == '':
                    break

                for i in range(len(expressions)):
                    match = re.findall(expressions[i],line)
                    if len(match) != 0:
                        matches[i] = match

        os.close(fd_r)
        os.close(fd_w)
    except:
        if verbose:
            tee.stdout.flush()
            raise


    command.communicate()
    sys.stdout.flush()
    if timedout:
        term.write("    [TIMEDOUT]\n")
    elif command.returncode == -signal.SIGSEGV:
        term.write("    [SEGFAULT]  \n")
    elif command.returncode != 0:
        term.write("    [FAILED]  \n")
    else:
        term.write("    [COMPLETE]\n")

    return matches

def execute_find2(command, expressions,verbose):
    if verbose:
        print(">",command)
    else:
        term.write("    [RUNNING]\r")

    pipe = subprocess.Popen(command, stdout=subprocess.PIPE,bufsize=1,shell=True)
    lines_iterator = iter(pipe.stdout.readline, b"")
    matches = [ None ] * len(expressions)
    while pipe.poll() is None:
        for line in lines_iterator:
            nline = line.decode("utf-8")
            sys.stdout.buffer.write(line);
            sys.stdout.buffer.flush()
            for i in range(len(expressions)):
                match = re.search(expressions[i],nline)
                if match != None:
                    matches[i] = match

    if pipe.returncode != 0:
        term.write("    [FAILED]  \n")
        sys.exit(pipe.returncode)
    else:
        term.write("    [COMPLETE]\n")

    return matches

def call(command,verbose):
    if verbose:
        print(">",command)
        failed = subprocess.call(command,shell=True)
    else:
        term.write("    [RUNNING]\r")
        failed = subprocess.call(command,shell=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
        if failed:
            term.write("    [FAILED]  \n")
            sys.exit(1)
        else:
            term.write("    [COMPLETE]\n")

def header(name):
    term_green="\x1B[32m"
    term_reset="\x1B[0m"
    term.write("{:s}{:s}{:s}\n".format(term_green,name,term_reset))

def require(file):
    try:
        os.stat(file)
    except:
        print("required file '{:s}' not found".format(file))
        print("-"*60)
        exc_type, exc_value, exc_traceback = sys.exc_info()
        traceback.print_tb(exc_traceback, limit=1, file=sys.stdout)
        print("-"*60)
        sys.exit(1)


