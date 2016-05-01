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

from argparse import ArgumentParser

__author__ = 'Shreyas Kulkarni'
__email__ = 'shyran@gmail.com'


class TreeConfig(object):
    def __init__(self):
        self._config = None
        self._parse_args()

    def _parse_args(self):
        parser = ArgumentParser()
        parser.add_argument('-s', '--show-hidden',
                            help="list hidden files and folders",
                            action='store_true',
                            default=False)

        parser.add_argument('--terse',
                            help="make it terse, visual pleasure is not desired",
                            action='store_true',
                            default=False)

        parser.add_argument('folders',
                            help='folders to draw tree for',
                            nargs='*',
                            default=['.'])

        parser.add_argument('-i', '--ignore',
                            help='ignore any file or folder that matches these wildcards',
                            nargs='*',
                            default=[])

        parser.add_argument('-f', '--filter',
                            help="filter and show *ONLY FILES* that match these wildcards",
                            nargs='+',
                            default=['*'])

        parser.add_argument('--ignore-empty',
                            help='ignore any empty folder (after filtering)',
                            action='store_true',
                            default=False)

        parser.add_argument('--tab',
                            help='how many spaces per tab. more the spaces, more spread out the tree',
                            type=int,
                            default=3)

        self._config = parser.parse_args()

    def show_hidden(self):
        return self._config.show_hidden

    def ignore_empty_directories(self):
        return self._config.ignore_empty

    def filter_patterns(self):
        return self._config.filter

    def ignore_patterns(self):
        return self._config.ignore

    def tabbing(self):
        return self._config.tab

    def folders(self):
        return self._config.folders

    def terse(self):
        return self._config.terse
