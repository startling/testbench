#!/usr/bin/env python
# -*- coding: utf-8 -*-

from testbench.runner import BenchmarkRunner
from clint.textui import colored, indent, puts


class ColorBenchmarkRunner(BenchmarkRunner):
    def output(self):
        """Print a bunch of statistics for each benchmark, nicely formatted and
        colored.
        """
        # for each benchmarked class/whatever
        for benchmark, results in self.run():
            print colored.cyan("Benchmarking `%s`..." % benchmark.__name__)
            print "=" * 80
            # for each set of arguments
            for argset in benchmark.arguments:
                print "With the argument set " + str(argset)
                print "-" * 80
                # these are all the Result objects for this argument set
                arg_results = [r for r in results if r.args == argset]
                stats = self.statistics(arg_results)
                # a function that scales a float into an int that will fit in
                # the console width (assume 80 for now).
                # 76 because 80 - 2 (for the brackets) - 2 (for the indent)
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
                            if time == these_stats.min:
                                color = colored.green
                            elif time == these_stats.max:
                                color = colored.red
                            else:
                                color = colored.cyan
                            # print a line for the number of seconds
                            puts("%s: %s" % (f.__name__, color("%f" % time))),
                            # print a bar to show what proportion of time this is
                            puts("[%s]" % color("=" * scaled(time)))
                print "-" * 80
            #TODO: scale for terminal width but still look pretty
