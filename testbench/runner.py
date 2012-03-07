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
