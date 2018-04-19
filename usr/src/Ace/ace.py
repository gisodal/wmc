#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import re
import fcntl
import subprocess
import argparse
from time import sleep

sys.path.append(os.path.dirname(os.path.realpath(__file__)))

import ply.lex as lex
import ply.yacc as yacc

def execute_find(cmd, expressions):

    fd_r, fd_w = os.pipe()
    command = subprocess.Popen(cmd,stdout=subprocess.PIPE)
    tee = subprocess.Popen(["tee", "/proc/{}/fd/{}".format(os.getpid(),fd_w)],
        stdin=command.stdout)

    fl = fcntl.fcntl(fd_r, fcntl.F_GETFL)
    fcntl.fcntl(fd_r, fcntl.F_SETFL, fl | os.O_NONBLOCK)
    output = os.fdopen(fd_r)

    matches = [[] for _ in range(len(expressions))]
    while tee.poll() is None:
        sleep(0.001)
        while True:
            line = output.readline()
            if line == '':
                break

            for i in range(len(expressions)):
                match = re.search(expressions[i],line)
                if match != None:
                    matches[i].append(match)

    os.close(fd_r)
    os.close(fd_w)

    command.communicate()
    if command.returncode != 0:
        print("execution failed...")

    return matches


class QueryParser():

    def __init__(self):
        lex.lex(module=self)
        yacc.yacc(module=self)

        self.variables = {}
        self.query_variable = {}

    # ===== lexical analyser =====
    tokens = ('NAME', 'GIVEN', 'AND', 'EQUALS')
    literals = ['=',',', '|']
    # t_ignore = "\t"

    t_GIVEN = r'\|'
    t_EQUALS = r'='
    t_AND = r','
    t_NAME = r'[^\|^=^,]+'

    def t_error(self,t):
        print("Illegal character '%s'" % t.value[0])
        t.lexer.skip(1)

    # ===== parser =====
    precedence = (
        ('left','AND'),
        ('left','EQUALS'),
        ('left','GIVEN')
    )

    def p_query_given(self,p):
        "query : query_assignment GIVEN assignments"
        pass

    def p_query(self,p):
        "query : assignments"
        pass

    def p_assignments(self,p):
        "assignments : assignment AND assignments"
        pass

    def p_assignments_closure(self,p):
        "assignments : assignment"
        pass

    def p_assignment(self,p):
        "assignment : NAME EQUALS NAME"
        self.variables[str.strip(p[1])] = str.strip(p[3])

    def p_query_assignement(self,p):
        "query_assignment : NAME EQUALS NAME"
        self.query_variable[str.strip(p[1])] = str.strip(p[3])

    def p_error(self,p):
        if(p):
            print("QUERY SYNTAX ERROR: line:", p.lexer.lineno, ",position:", p.lexpos, ", syntax error:", p.value)
        else:
            print("QUERY UNKNOWN SYNTAX ERROR: Unknown syntax error")
        sys.exit(1)

    def print_tokens(self,query):
        lex.input(query)
        while True:
            tok = lex.token()
            if not tok:
                break

            print(tok)

    def parse(self,query):
        yacc.parse(query)

    def clear(self):
        self.variables.clear()
        self.query_variable.clear()

class Ace():
    def __init__(self):
        self.parser = QueryParser()
        self.dir = os.path.abspath(os.path.dirname(os.path.realpath(__file__)))
        self.network_dir = os.path.join(self.dir,"networks")
        self.inference   = os.path.join(self.dir,"ace_v3.0_linux86/evaluate")
        self.compiler    = os.path.join(self.dir,"ace_v3.0_linux86/compile")

    def parse(self, query_string):
        self.parser.clear()
        if query_string:
            self.parser.parse(query_string)

        return [self.parser.query_variable,self.parser.variables]

    def write_query(self,filename,query,with_query_variable):
        f = open(filename,'w')
        f.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n")
        f.write("<instantiation>\n")

        if with_query_variable:
            for variable,value in query[0].items():
                f.write("    <inst id=\"{0}\" value=\"{1}\"/>\n".format(variable,value))

        for variable,value in query[1].items():
            f.write("    <inst id=\"{0}\" value=\"{1}\"/>\n".format(variable,value))

        f.write("</instantiation>\n")
        f.close()

    def is_compiled(self,hugin):
        return os.path.exists("{0}.{1}".format(hugin,"ac")) and os.path.exists("{0}.{1}".format(hugin,"lmap"))


    def compile_cmd(self,cmd):
        regex_time = r'Compile Time \(s\) : ([.0-9]+)'
        regex_init = r'Initialization Time \(s\) : ([.0-9]+)'
        matches = execute_find(cmd, [regex_time,regex_init])

        init_time = float(matches[1][0].groups()[0])
        compile_time = float(matches[0][0].groups()[0])
        return compile_time # + init_time

    def compile(self,options):
        if options.compile or options.overwrite or not self.is_compiled(options.hugin):
            cmd = [self.compiler,hugin]
            return self.compile_cmd(cmd);


    def compile_c2d(self,options):
        if options.compile or options.overwrite or not self.is_compiled(options.hugin):
            cmd = [self.compiler,'-forceC2d','-noEclause',options.hugin]
            return self.compile_cmd(cmd);

    def posterior(self,hugin,query_str):
        instfile = []
        query = self.parse(query_str)

        if len(query[0]) > 0 or len(query[1]) > 0:
            print("## compute P({})".format(query_str))
            instfile.append("{0}.{1}".format(hugin,"0.inst"))
            self.write_query(instfile[0], query,True)
            if len(query[0]) > 0:
                instfile.append("{0}.{1}".format(hugin,"1.inst"))
                self.write_query(instfile[1], query,False)
            elif len(query[1]) == 1:
                bquery = query
                bquery[0] = bquery[1]
                bquery[1] = {}
                instfile.append("{0}.{1}".format(hugin,"1.inst"))
                self.write_query(instfile[1], bquery,False)


        cmd = [self.inference,hugin]
        cmd.extend(instfile)

        regex_probability = r'Pr\(e\) = ([\+\-E.0-9]+)'
        regex_time = r'Total Inference Time \(ms\) : ([.0-9]+)'
        regex_init = r'Total Initialization Time \(ms\) : ([.0-9]+)'
        matches = execute_find(cmd, [regex_probability,regex_time,regex_init])

        first = float(matches[0][0].groups()[0])
        compile_time = float(matches[1][0].groups()[0])
        init_time = float(matches[2][0].groups()[0])
        time = compile_time
        if len(matches[0]) == 2:
            second = float(matches[0][1].groups()[0])
            return first/second,time
        else:
            return first,time


def main():
    parser = argparse.ArgumentParser(description='ACE interface',add_help=False)

    parser.add_argument('--help',action='help',help='Show this help message and exit')
    parser.add_argument('--network',dest='hugin', help='Bayesian network(s) used for testing',metavar="HUGIN")
    parser.add_argument('--overwrite',dest='overwrite',action='store_true', help='Overwrite compiled circuit')
    parser.add_argument('--compile',dest='compile',action='store_true', help='Only compile')
    parser.add_argument('--no-c2d',dest='noc2d',action='store_true', help='Do not compile with c2d')
    parser.add_argument('--query',dest='query',nargs=argparse.REMAINDER, help="Query of the form VAR = VALUE [[|,] VAR = VALUE [, ...]]")

    if len(sys.argv)==1:
        parser.print_help()
        sys.exit(0)

    options = parser.parse_args()
    if options.hugin == None:
        parser.error('{} requires --network'.format(options.test))

    if options.query != None:
        options.query = " ".join(options.query)

    if not os.path.exists(options.hugin):
        parser.error('network "{}" not found'.format(options.hugin))

    ace = Ace()
    if options.noc2d:
        compile_time = ace.compile(options)
    else:
        compile_time = ace.compile_c2d(options)

    if options.compile:
        print("Compilation result:")
        print("===================")
        print("Total time: {0}s".format(compile_time))
        print("Total time: {0}ms".format(float(compile_time)*1000))
    else:
        probability,time = ace.posterior(options.hugin,options.query)
        print("Result for P({0})".format(options.query))
        print("===================")
        print("Prob : {0}".format(probability))
        print("Time : {0} s".format(float(time)*0.001))





main();

