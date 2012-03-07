#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time


def benchmark(fn):
    "A decorator that sets the `benchmark_this` flag on a function."
    fn._benchmark_this = True
    return fn

class Benchmark(object):
    """A class for benchmarks that will be run by testbench. Things don't
    really need to be subclasses of this, they just need to implement
    __benchmark__. 
    """
    # `arguments` needs to be any iterable that gives tuples or lists
    # of arguments to be applied to each benchmark method.
    arguments = []
    #TODO: keyword arguments

    # the amount of times to run each method with each argument set
    repetitions = 100

    @classmethod
    def _trial(cls, method, args):
        """Given a method and some arguments, run and time a single trial of
        that method with those arguments.
        """
        # instantiate the class
        obj = cls()
        # start the timer!
        start = time.time()
        # call the method with the arguments
        method(obj, *args)
        # and return the time it took
        return time.time() - start

    @classmethod
    def get_methods(cls):
        """Return an iterator that contains the methods that we should
        benchmark; here, the ones with the ._benchmark_this flag.
        """
        # get all the methods that have the _benchmark_this flag
        for method in (getattr(cls, m) for m in dir(cls)):
            if hasattr(method, "_benchmark_this"):
                yield method

    @classmethod
    def __benchmark__(cls):
        """Run each method that has the ._benchmark_this flag `repetitions`
        times, with each of the given arguments. Return a dictionary with 
        methods as keys and lists as values; each of these lists represents
        the given argument set in that position. Each of the argument set
        lists contain some floats for the length of time that method took
        with those arguments on that trial.
        """
        results = {}
        for method in cls.get_methods():
            # add the method to the `results` dict
            results[method] = []
            # for each given argument
            for args in cls.arguments:
                # append an empty list for the results with this argument
                results[method].append([])
                # for each repetition
                for n in xrange(cls.repetitions):
                    # append the results to the list for this argument set
                    trial_results = cls._trial(method, args)
                    results[method][-1].append(trial_results)
        return results
