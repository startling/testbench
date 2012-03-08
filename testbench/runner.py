#!/usr/bin/env python
# -*- coding: utf-8 -*-

from collections import namedtuple
from testbench import Benchmark
from testbench.utilities import avg


class BenchmarkRunner(object):
    stat_functions = [min, avg, max]

    def __init__(self, module):
        "Given a module to run on, initialize this BenchmarkRunner."
        self.module = module

    def discover(self):
        "Get all the objects from self.module that implement `__benchmark__`"
        # for each of the actual objects in the module
        for o in (getattr(self.module, a) for a in dir(self.module)):
            # yield all of the things that a) implement __benchmark__ and
            # b) are not the base 
            #TODO: find a better way to exclude base classes, rather than just
             # specialcasing Benchmark. Maybe we should just ignore the ones 
             # that don't yield anything in their .get_methods?
            if hasattr(o, "__benchmark__") and o is not Benchmark:
                yield o
    
    def run(self):
        for benchmark in self.discover():
            self.output(benchmark, benchmark.__benchmark__())

    def output(self, benchmark, results):
        "Given a benchmark and its results, print and format some statistics."
        print "=" * 80
        print "Benchmarking %s..." % benchmark.__name__
        print "=" * 80
        # for each set of arguments
        for argset in benchmark.arguments:
            print "For the argument set " + str(argset)
            print "-" * 80
            # for each result that used this set of arguments.
            for r in (r for r in results if r.args == argset):
                print "%s:" % r.method.__name__,
                # print a line with all of the stat_functions
                for f in self.stat_functions:
                    print "%s: %f" % (f.__name__, f(r.results)),
                print
            print "-" * 80
        #TODO: organize things so users can set grouping

    def statistics(self, results):
        """Given a list of list of Results, return a named three-tuple with the
        an item with the name of each function in self.stat_functions. Each of
        these items is itself a similar three-tuple, but each item is, e.g.,
        the maximum of the maximums of the results.
        """
        nt = namedtuple("Statistic", [n.__name__ for n in self.stat_functions])
        s = []
        for f_one in self.stat_functions:
            inside = []
            for f_two in self.stat_functions:
                inside.append(f_two(f_one(r.results) for r in results))
            s.append(nt(*inside))
        return nt(*s)
