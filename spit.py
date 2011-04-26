#!/usr/bin/env python

import ast
import sys

print ast.dump(ast.parse(sys.argv[1]))

