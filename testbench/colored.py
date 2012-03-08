#!/usr/bin/env python
# -*- coding: utf-8 -*-

from testbench.runner import BenchmarkRunner
from clint.textui import colored, indent, puts


class ColorBenchmarkRunner(BenchmarkRunner):
    def handle_benchmark(self, benchmark, results):
        """Given a benchmark and its results, print nicely-formatted and
        colored statistics.
        """
        print colored.cyan("Benchmarking `%s`..." % benchmark.__name__)
        print "=" * 80
        # for each set of arguments
        #TODO: don't reference benchmark.arguments ever; it could be any
        # iterator that yields some values, for all we know.
        for argset in benchmark.arguments:
            print "With the argument set " + str(argset)
            print "-" * 80
            # these are all the Result objects for this argument set
            arg_results = [r for r in results if r.args == argset]
            stats = self.statistics(arg_results)
            # a function that scales a float into an int that will fit in
            # the console width (assume 80 for now).
            # 76 because 80 - 2 (for the brackets) - 2 (for the indent)
            #TODO: don't depend on stats having a `max` field here.
            scaled = lambda x: int(76 * (x/stats.max.max))
            # for each 
            for r in arg_results:
                print "%s:" % colored.cyan(r.method.__name__)
                with indent(2):
                    # for each of the statistic functions
                    for f in self.stat_functions:
                        time = f(r.results)
                        # get the statistics for this stat function
                        these_stats = getattr(stats, f.__name__)
                        # the color is green if it's the fastest, red if
                        # it's the slowest, and cyan otherwise
                        if time == getattr(these_stats, "min", 0.):
                            color = colored.green
                        elif time == getattr(these_stats, "max", None):
                            color = colored.red
                        else:
                            color = colored.cyan
                        # print a line for the number of seconds
                        puts("%s: %s" % (f.__name__, color("%f" % time))),
                        # print a bar to show what proportion of time this is
                        puts("[%s]" % color("=" * scaled(time)))
            print "-" * 80
            #TODO: scale for terminal width but still look pretty
