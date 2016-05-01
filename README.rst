===============================
lstree
===============================

.. image:: https://img.shields.io/pypi/v/lstree.svg
        :target: https://pypi.python.org/pypi/lstree

.. image:: https://img.shields.io/travis/shreyas/lstree.svg
        :target: https://travis-ci.org/shreyas/lstree

.. image:: https://readthedocs.org/projects/lstree/badge/?version=latest
        :target: https://readthedocs.org/projects/lstree/?badge=latest
        :alt: Documentation Status


lstree is for ls what pstree is for ps, and some more ...

The idea struck when I had just started using leiningen for creating a clojure project. I wanted a way to see what all files/folders/things are created when leiningen creates a project. So I wrote this tool. It helps you visually see the folder hierarchy, and allows you to do some basic filtering on the tree. 

* Free software: MIT license
* Documentation: https://lstree.readthedocs.org.

Features
--------

* Show a folder (or many, if specified) in tree structure
* Show/hide hidden files 
* Ignore empty directories
* Show (filter for) only certain files
* Ignore certain files/folders

Installation
------------

Use pip to install lstree::

    pip install lstree


Basic Usage
-----------

lstree when used without any arguments, shows the current tree for $PWD::

    tochukasui:hello-world$ lstree
    |- ./
       |- doc/
          |- intro.md

       |- resources/
       |- src/
          |- hello_world/
             |- core.clj

       |- target/
          |- base+system+user+dev/
             |- classes/
                |- META-INF/
                   |- maven/
                      |- hello-world/
                         |- hello-world/
                            |- pom.properties

             |- stale/
                |- leiningen.core.classpath.extract-native-dependencies

          |- classes/
             |- META-INF/
                |- maven/
                   |- hello-world/
                      |- hello-world/
                         |- pom.properties

          |- stale/
             |- leiningen.core.classpath.extract-native-dependencies

          |- hello-world-0.1.0-SNAPSHOT.jar

       |- test/
          |- hello_world/
             |- core_test.clj

       |- CHANGELOG.md
       |- LICENSE
       |- project.clj
       |- README.md

Apparently this was a hello-world lein project after a `lein build`. Too much clutter. I don't care of about anything inside the target folder anyway. Let's cut it out::

    tochukasui:hello-world$ lstree -i target
    |- ./
       |- doc/
          |- intro.md

       |- resources/
       |- src/
          |- hello_world/
             |- core.clj

       |- test/
          |- hello_world/
             |- core_test.clj

       |- CHANGELOG.md
       |- LICENSE
       |- project.clj
       |- README.md

Much better. We '-i gnored' the target folder. How about just focusing on the clojure source files?::

    tochukasui:hello-world$ lstree -i target -f '*.clj'
    |- ./
       |- doc/
       |- resources/
       |- src/
          |- hello_world/
             |- core.clj

       |- test/
          |- hello_world/
             |- core_test.clj

       |- project.clj

Nice. But what are those 'doc' and 'resources' folders doing there? They don't have any clj files; why clutter the view?::

    tochukasui:hello-world$ lstree -i target -f '*.clj' --ignore-empty
    |- ./
       |- src/
          |- hello_world/
             |- core.clj

       |- test/
          |- hello_world/
             |- core_test.clj

       |- project.clj

Aha! 

There are a few more useful tools lstree offers. For more info, check out the usage section of the documentation: https://lstree.readthedocs.io/en/latest/usage.html
