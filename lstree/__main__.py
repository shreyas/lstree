#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2016 Shreyas Kulkarni (shyran@gmail.com)
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import os
import sys
from lstree.nodetree.builder import NodeTreeBuilder
from lstree.nodetree.plotter import NodeTreePlotter
from treeconfig import TreeConfig

__author__ = 'Shreyas Kulkarni'
__email__ = 'shyran@gmail.com'


def main():
    config = TreeConfig()
    plotter = NodeTreePlotter(config)

    # we can work with multiple root folders
    # (./ being the default if none is provided)
    for rf in config.folders():
        # a minor tweak to sweeten the output
        root_folder = rf.strip(os.path.sep)

        try:
            builder = NodeTreeBuilder(root_folder, config)
            root_node = builder.build()
            root_node.visit(plotter)

        except RuntimeError as rte:
            print("error: " + rte.message)
            return -1


if __name__ == '__main__':
    sys.exit(main() or 0)
