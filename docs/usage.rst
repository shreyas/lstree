=====
Usage
=====


lstree is a command line utility to show a folder structure in tree form. This is useful when you are working on a project that involvs many files and folders. 

Here is an example lstree use::

    tochukasui:testbed$ lstree 
    |- ./
       |- emptydir/
       |- somedir/
          |- somefile.compiled
          |- somefile1
          |- somefile2
          |- somefile3

       |- datafile.xml
       |- ignore.me.compiled
       |- testfile

If you want to see hidden files, use -s::

    tochukasui:testbed$ lstree -s
    |- ./
       |- .hiddendir/
          |- .hiddenfile
          |- .hiddenfile.compiled

       |- emptydir/
       |- somedir/
          |- somefile.compiled
          |- somefile1
          |- somefile2
          |- somefile3

       |- datafile.xml
       |- ignore.me.compiled
       |- testfile

For applying a wildcard filter to the folder contents, use -f options::

    tochukasui:testbed$ lstree -f '*.compiled' 'data*'
    |- ./
       |- emptydir/
       |- somedir/
          |- somefile.compiled

       |- datafile.xml
       |- ignore.me.compiled

For ignoring files and directories, use -i option::

    tochukasui:testbed$ lstree -i somefile* 'data*' 
    |- ./
       |- emptydir/
       |- somedir/
       |- ignore.me.compiled
       |- testfile

To ignore empty folder, there is --ignore-empty option::

    tochukasui:testbed$ lstree -i somefile* 'data*' --ignore-empty
    |- ./
       |- ignore.me.compiled
       |- testfile

For help, use -h::

    tochukasui:testbed$ lstree -h
    usage: lstree [-h] [-s] [--terse] [-i [IGNORE [IGNORE ...]]]
                  [-f [FILTER [FILTER ...]]] [--ignore-empty] [--tab TAB]
                  [folders [folders ...]]

    positional arguments:
      folders               folders to draw tree for

    optional arguments:
      -h, --help            show this help message and exit
      -s, --show-hidden     list hidden files and folders
      --terse               make it terse, visual pleasure is not desired
      -i [IGNORE [IGNORE ...]], --ignore [IGNORE [IGNORE ...]]
                            ignore any file or folder that matches these wildcards
      -f [FILTER [FILTER ...]], --filter [FILTER [FILTER ...]]
                            filter and show *ONLY FILES* that match these
                            wildcards
      --ignore-empty        ignore any empty folder (after filtering)
      --tab TAB             how many spaces per tab. more the spaces, more spread
                            out the tree

Specifying --terse gets rid of all new lines that are added to space out the tree::

    tochukasui:testbed$ lstree -s --terse
    |- ./
       |- .hiddendir/
          |- .hiddenfile
          |- .hiddenfile.compiled
       |- emptydir/
       |- somedir/
          |- somefile.compiled
          |- somefile1
          |- somefile2
          |- somefile3
       |- datafile.xml
       |- ignore.me.compiled
       |- testfile

While --tab option allows you to shrink or spread out the tree horizontally::

    tochukasui:testbed$ lstree -s --terse --tab 6
    |- ./
          |- .hiddendir/
                |- .hiddenfile
                |- .hiddenfile.compiled
          |- emptydir/
          |- somedir/
                |- somefile.compiled
                |- somefile1
                |- somefile2
                |- somefile3
          |- datafile.xml
          |- ignore.me.compiled
          |- testfile
    tochukasui:testbed$ 
