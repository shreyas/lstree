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

import abc

from lstree.nodetree.visitor import NodeTreeVisitor

__author__ = 'Shreyas Kulkarni'
__email__ = 'shyran@gmail.com'


class Node(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self, name):
        self._name = name
        self._children = []

    def name(self):
        return self._name

    def __repr__(self):
        return self.name()

    def __add__(self, other):
        assert issubclass(other.__class__, Node)
        self._children.append(other)

        return self

    @abc.abstractmethod
    def empty(self):
        pass

    def prune(self, predicate):
        """
        allow a visitor predicate to choose candidates to prune
        then prune the chosen ones out
        :param predicate: any function that takes in a Node and returns True or False
        :return: nothing
        """
        # send it downwards first. process at the leaf nodes first, then bubble up
        for c in self._children:
            c.prune(predicate)

        # now actually prune children that match the predicate
        self._children = [c for c in self._children if not predicate(c)]

    def visit(self, visitor, topdown=True):
        """
        allow a visitor to visit each node in the node-tree in a top-down fashion (by default)
        :param visitor: an instance of NodeTreeVisitor which knows what to do when visiting each type of the nodes
        :param topdown: from top towards bottom if True, bottom-up if False
        :return: nothing
        """
        assert isinstance(visitor, NodeTreeVisitor)

        if topdown:
            # first visit self, if it's top-down
            visitor.visit(self)

        if len(self._children):
            visitor.down()

            # visit the children
            for c in self._children:
                c.visit(visitor, topdown)

            visitor.up()

        if not topdown:
            # if it's bottom-up, then visit self last
            visitor.visit(self)
