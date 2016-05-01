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

from lstree.nodes.file import FileNode
from lstree.nodes.node import Node

__author__ = 'Shreyas Kulkarni'
__email__ = 'shyran@gmail.com'


class DirectoryNode(Node):
    def __init__(self, name):
        super(DirectoryNode, self).__init__(name)

    def __repr__(self):
        return self.name() + os.sep

    def file_count(self):
        """
        :return: count of all FileNodes
        """
        # TODO: hard dependency!! can be refactored?
        return len([node for node in self._children if type(node) is FileNode])

    def directories(self):
        """
        :return: list of all DirectoryNodes
        """
        return [node for node in self._children if type(node) is DirectoryNode]

    def empty(self):
        """
        a directory node is empty if it doesn't contain any file and all its subdirectories
        are empty as well
        :return: True if the directory hierarchy is empty
        """
        if len(self._children) < 1:
            return True

        return self.file_count() == 0 and all([d.empty() for d in self.directories()])
