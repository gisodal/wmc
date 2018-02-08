#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os

SCRIPT_DIR = os.path.abspath(
    os.path.join(
        os.path.dirname(
            os.path.realpath(__file__)),".."
        )
    )

WMC_DIR = os.path.abspath(os.path.join(SCRIPT_DIR,".."))

DATA_DIR = os.path.join(WMC_DIR,"data")

NET_DIR = os.path.join(DATA_DIR,"net")


