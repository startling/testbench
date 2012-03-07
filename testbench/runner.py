#!/usr/bin/env python
# -*- coding: utf-8 -*-

from testbench import Benchmark


class BenchmarkRunner(object):
    def discover(self, module):
        "Given a module, get all the objects that implement `__benchmark__`"
        # for each of the actual objects in the module
        for o in (getattr(module, a) for a in dir(module)):
            # yield all of the things that a) implement __benchmark__ and
            # b) are not the base 
            #TODO: find a better way to exclude base classes, rather than just
             # specialcasing Benchmark. Maybe we should just ignore the ones 
             # that don't yield anything in their .get_methods?
            if hasattr(o, "__benchmark__") and o is not Benchmark:
                yield o
