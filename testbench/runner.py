#!/usr/bin/env python
# -*- coding: utf-8 -*-

from testbench import Benchmark


class BenchmarkRunner(object):
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


def average(iterable):
    "A generic `average` function that works on any iterable, including iterators."
    total = float(0)
    count = float(0)
    for n in iterable:
        total += n
        count += 1
    return total/count
