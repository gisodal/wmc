#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys

SCRIPT_DIR = os.path.abspath(
    os.path.join(
        os.path.dirname(
            os.path.realpath(__file__)),".."
        )
    )

WMC_DIR = os.path.abspath(os.path.join(SCRIPT_DIR,".."))
while not os.path.exists(os.path.join(WMC_DIR,"data")) and WMC_DIR is not '/':
    WMC_DIR = os.path.abspath(os.path.join(WMC_DIR,".."))

if WMC_DIR == '/':
    sys.stderr.write("FATAL: Main data directory count not be determined")
    sys.exit(1)

DATA_DIR = os.path.join(WMC_DIR,"data")
NET_DIR = os.path.join(DATA_DIR,"net")

