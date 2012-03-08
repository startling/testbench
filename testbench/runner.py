#!/usr/bin/env python
# -*- coding: utf-8 -*-

from collections import namedtuple
from testbench import Benchmark
from testbench.utilities import average


class BenchmarkRunner(object):
    stat_functions = [min, average, max]

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
            yield (benchmark, benchmark.__benchmark__())

    def output(self):
        for benchmark, results in self.run():
            print "=" * 80
            print "Benchmarking %s..." % benchmark.__name__
            print "=" * 80
            argsets = benchmark.arguments
            for argset in argsets:
                print "For the argument set " + str(argset)
                print "-" * 80
                for r in (r for r in results if r.args == argset):
                    print "%s:" % r.method.__name__,
                    print "avg:",
                    print "%f" % average(r.results)
                    print "max: %f" % max(r.results),
                    print "min: %f" % min(r.results)
                print "-" * 80

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
