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

from lstree.nodes.file import FileNode
from lstree.nodetree.visitor import NodeTreeVisitor

__author__ = 'Shreyas Kulkarni'
__email__ = 'shyran@gmail.com'


class NodeTreePlotter(NodeTreeVisitor):
    def __init__(self, config):
        self.level = 0
        self._config = config
        self._last_visited = None

    def prefix(self):
        return ' ' * self.level * self._config.tabbing() + '|- '

    def up(self):
        self.level -= 1

        # add a line for visually pleasing plotting (if not in terse mode)
        if type(self._last_visited) is FileNode and not self._config.terse():
            print
            self._last_visited = None

    def down(self):
        self.level += 1

    def visit(self, node):
        print(self.prefix() + repr(node))
        self._last_visited = node
