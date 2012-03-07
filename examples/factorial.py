#!/usr/bin/env python
# -*- coding: utf-8 -*-

from testbench import Benchmark, benchmark


class Factorial(Benchmark):
    arguments = [(5,), (125,), (200,)]

    @benchmark
    def iterative_factorial(self, n):
        total = 1
        for number in xrange(1, n + 1):
            total *= number
        return total

    @benchmark
    def recursive_factorial(self, n):
        if n == 1:
            return 1
        else:
            return n * self.recursive_factorial(n - 1)
