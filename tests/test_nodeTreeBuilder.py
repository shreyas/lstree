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

from unittest import TestCase
import unittest
from lstree.nodetree.builder import NodeTreeBuilder
from lstree.nodetree.visitor import NodeTreeVisitor
from lstree.treeconfig import TreeConfig

__author__ = 'Shreyas Kulkarni'
__email__ = 'shyran@gmail.com'


class TestNodeTreeBuilder(TestCase):
    class PatchedNodeTreeBuilder(NodeTreeBuilder):
        def _load_os_walk_cache(self):
            self._os_walk_cache = {'./.hiddendir': ([],
                                                    ['.hiddenfile', '.hiddenfile.compiled']),
                                   './emptydir': ([], []),
                                   './somedir': ([],
                                                 ['somefile.compiled', 'somefile1', 'somefile2', 'somefile3']),
                                   '.': (['.hiddendir', 'emptydir', 'somedir'],
                                         ['datafile.xml', 'ignore.me.compiled', 'testfile'])}

    class MockedTreeConfig(TreeConfig):
        """
        mocking with unittest.mock is not useful since the builder checks instance of
        incoming config with isinstance. so we inherit to mock
        """
        def __init__(self,
                     show_hidden=False,
                     ignore_empty_directories=False,
                     filter_patterns=['*'],
                     ignore_patterns=[],
                     tabbing=3,
                     folders=["doesn't matter"],
                     terse=False,):
            self._show_hidden = show_hidden
            self._ignore_empty_directories = ignore_empty_directories
            self._filter_patterns = filter_patterns
            self._ignore_patterns = ignore_patterns
            self._tabbing = tabbing
            self._folders = folders
            self._terse = terse

        def terse(self): return self._terse

        def filter_patterns(self): return self._filter_patterns

        def folders(self): return self._folders

        def tabbing(self): return self._tabbing

        def ignore_empty_directories(self): return self._ignore_empty_directories

        def ignore_patterns(self): return self._ignore_patterns

        def show_hidden(self): return self._show_hidden

    class NodesAccumulator(NodeTreeVisitor):
        def __init__(self):
            # this is where we collect all nodes
            self._nodes_cache = set()

        def visit(self, node):
            super(TestNodeTreeBuilder.NodesAccumulator, self).visit(node)
            self._nodes_cache.add(node.name())

        def __contains__(self, item):
            return item in self._nodes_cache

    def test_build(self):
        mocked_config = self.MockedTreeConfig()
        patched_builder = self.PatchedNodeTreeBuilder(root_dir=".",
                                                      config=mocked_config)

        root = patched_builder.build()

        nodes = self.NodesAccumulator()
        root.visit(nodes)

        # ensure what's in
        self.assertTrue('emptydir' in nodes)
        self.assertTrue('somedir' in nodes)
        self.assertTrue('somefile.compiled' in nodes)
        self.assertTrue('somefile1' in nodes)
        self.assertTrue('somefile2' in nodes)
        self.assertTrue('somefile3' in nodes)
        self.assertTrue('datafile.xml' in nodes)
        self.assertTrue('ignore.me.compiled' in nodes)
        self.assertTrue('testfile' in nodes)

        # also ensure what stays out
        self.assertTrue('.hiddendir' not in nodes)
        self.assertTrue('.hiddenfile' not in nodes)
        self.assertTrue('.hiddenfile.compiled' not in nodes)

    def test_build_show_hidden(self):
        mocked_config = self.MockedTreeConfig(show_hidden=True)
        patched_builder = self.PatchedNodeTreeBuilder(root_dir=".",
                                                      config=mocked_config)

        root = patched_builder.build()

        nodes = self.NodesAccumulator()
        root.visit(nodes)

        # ensure what's in
        self.assertTrue('emptydir' in nodes)
        self.assertTrue('somedir' in nodes)
        self.assertTrue('somefile.compiled' in nodes)
        self.assertTrue('somefile1' in nodes)
        self.assertTrue('somefile2' in nodes)
        self.assertTrue('somefile3' in nodes)
        self.assertTrue('datafile.xml' in nodes)
        self.assertTrue('ignore.me.compiled' in nodes)
        self.assertTrue('testfile' in nodes)

        # also ensure that hidden files are listed as well
        self.assertTrue('.hiddendir' in nodes)
        self.assertTrue('.hiddenfile' in nodes)
        self.assertTrue('.hiddenfile.compiled' in nodes)

    def test_build_ignore_empty(self):
        mocked_config = self.MockedTreeConfig(ignore_empty_directories=True)
        patched_builder = self.PatchedNodeTreeBuilder(root_dir=".",
                                                      config=mocked_config)

        root = patched_builder.build()

        nodes = self.NodesAccumulator()
        root.visit(nodes)

        # ensure what's in
        self.assertTrue('somedir' in nodes)
        self.assertTrue('somefile.compiled' in nodes)
        self.assertTrue('somefile1' in nodes)
        self.assertTrue('somefile2' in nodes)
        self.assertTrue('somefile3' in nodes)
        self.assertTrue('datafile.xml' in nodes)
        self.assertTrue('ignore.me.compiled' in nodes)
        self.assertTrue('testfile' in nodes)

        # also ensure that hidden files are listed as well
        self.assertTrue('emptydir' not in nodes)
        self.assertTrue('.hiddendir' not in nodes)
        self.assertTrue('.hiddenfile' not in nodes)
        self.assertTrue('.hiddenfile.compiled' not in nodes)

    def test_build_ignore_patterns(self):
        """
        we can supply multiple wildcard patterns to be ignored
        they can be: file.*, partialname*, directoryname etc
        """
        mocked_config = self.MockedTreeConfig(ignore_patterns=['*.compiled',
                                                               'data*',
                                                               'somedir'])
        patched_builder = self.PatchedNodeTreeBuilder(root_dir=".",
                                                      config=mocked_config)

        root = patched_builder.build()

        nodes = self.NodesAccumulator()
        root.visit(nodes)

        # ensure what's in
        self.assertTrue('emptydir' in nodes)
        self.assertTrue('testfile' in nodes)

        # also ensure that hidden files are listed as well
        self.assertTrue('somedir' not in nodes)
        self.assertTrue('somefile1' not in nodes)
        self.assertTrue('somefile2' not in nodes)
        self.assertTrue('somefile3' not in nodes)
        self.assertTrue('datafile.xml' not in nodes)
        self.assertTrue('somefile.compiled' not in nodes)
        self.assertTrue('ignore.me.compiled' not in nodes)
        self.assertTrue('.hiddendir' not in nodes)
        self.assertTrue('.hiddenfile' not in nodes)
        self.assertTrue('.hiddenfile.compiled' not in nodes)

    def test_build_filter_patterns(self):
        """
        filter patterns are used as positive filters, i.e. to seek out
        only those files that match the given pattern
        these patterns can be specified similar to ignore patterns
        """
        mocked_config = self.MockedTreeConfig(filter_patterns=['*.compiled',
                                                               'data*'])
        patched_builder = self.PatchedNodeTreeBuilder(root_dir=".",
                                                      config=mocked_config)

        root = patched_builder.build()

        nodes = self.NodesAccumulator()
        root.visit(nodes)

        # ensure what's in
        self.assertTrue('emptydir' in nodes)        # empty dirs are still listed (unless ignored)
        self.assertTrue('somedir' in nodes)

        self.assertTrue('datafile.xml' in nodes)
        self.assertTrue('somefile.compiled' in nodes)
        self.assertTrue('ignore.me.compiled' in nodes)

        # also ensure that hidden files are listed as well
        self.assertTrue('testfile' not in nodes)
        self.assertTrue('somefile1' not in nodes)
        self.assertTrue('somefile2' not in nodes)
        self.assertTrue('somefile3' not in nodes)
        self.assertTrue('.hiddendir' not in nodes)
        self.assertTrue('.hiddenfile' not in nodes)
        self.assertTrue('.hiddenfile.compiled' not in nodes)


if __name__ == '__main__':
    import sys
    sys.exit(unittest.main())
