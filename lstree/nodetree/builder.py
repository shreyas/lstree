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

from fnmatch import fnmatch
import os

from lstree.nodes.directory import DirectoryNode
from lstree.nodes.file import FileNode
from lstree.treeconfig import TreeConfig

__author__ = 'Shreyas Kulkarni'
__email__ = 'shyran@gmail.com'


class NodeTreeBuilder(object):
    def __init__(self, root_dir, config):
        assert isinstance(config, TreeConfig)

        self._root_dir = root_dir
        self._config = config

        self._load_os_walk_cache()

    def _load_os_walk_cache(self):
        """
        use os.walk to get files and folders within the root dir
        builds a usable map before building a tree

        :return: nothing (changes state)
        """
        self._os_walk_cache = {a[0]: (a[1], a[2]) for a in os.walk(self._root_dir)}
        # print str(self._os_walk_cache)

    def build(self):
        """
        :param root_dir: root directory to start building from
        :return: built node tree
        """
        # build the node tree starting from the root directory
        root = self._build_directory(self._root_dir)

        # apply all filters
        if not self._config.show_hidden():
            root.prune(lambda node: node.name().startswith('.') and len(node.name()) > 0)

        # 'and'ing ignore patterns
        for pattern in self._config.ignore_patterns():
            root.prune(lambda node: fnmatch(node.name(), pattern))

        # 'or'ing the filter patterns
        root.prune(lambda node: isinstance(node, FileNode) and
                                not any([fnmatch(node.name(), pattern)
                                         for pattern in self._config.filter_patterns()]))

        if self._config.ignore_empty_directories():
            root.prune(lambda node: isinstance(node, DirectoryNode) and node.empty())

        return root

    def _build_directory(self, dirname):
        """
        :param dirname: directory name
        :param level: tabbing level for the directory
        :return: built DirectoryNode
        """
        # check if all's well
        if dirname not in self._os_walk_cache:
            raise RuntimeError("directory " + dirname + " not found")

        dnode = DirectoryNode(os.path.basename(dirname))

        dirs, files = self._os_walk_cache[dirname]
        for d in dirs:
            dnode += self._build_directory(os.path.join(dirname, d))

        for f in files:
            dnode += FileNode(f)

        return dnode
