from __future__ import print_function

import os


__author__ = ["tom van mele"]
__copyright__ = "ETH Zurich - Block Research Group"
__license__ = "MIT License"
__email__ = "tom.v.mele@gmail.com"
__version__ = "0.1.0"


designers = []
developers = []
documenters = []
title = "RhinoVAULT"
website = "https://blockresearchgroup.gitbook.io/rhinovault"
description = "Rhino plugin for form finding of compression-only structures using Thrust Network Analysis."


HERE = os.path.dirname(__file__)

HOME = os.path.abspath(os.path.join(HERE, "../../"))
DATA = os.path.abspath(os.path.join(HOME, "data"))
DOCS = os.path.abspath(os.path.join(HOME, "docs"))
TEMP = os.path.abspath(os.path.join(HOME, "temp"))


__all__ = ["HOME", "DATA", "DOCS", "TEMP"]
