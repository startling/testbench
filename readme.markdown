# Testbench

**Testbench** is a benchmarking library for python inspired by unittest.

It's not quite there yet, but it will be.

## Installation

Using pip, you can install straight from this repository:

````
pip install git+git://github.com/startling/testbench.git
````

Or you can clone the repository and install it as editable, if you want to play with the source:

````
git clone git://github.com/startling/testbench.git
pip install -e testbench
````

## Usage
Write a python script, include it in your package, and run `testbench mypackaged.benchmarks` or `testbench-color mypackage.benchmarks`.

Say we want to determine the fastest way to get the factorial of `n`. Here's the kind of thing we would write:

````python
#!/usr/bin/env python
# -*- coding: utf-8 -*-

from testbench import Benchmark, benchmark
from math import factorial


class Factorial(Benchmark):
    # a list of argument-tuples that we'll feed to each method, one at a time
    arguments = [(5,), (125,), (200,)]

    # decorate a function with @benchmark so it will get benchmarked. simple enough.
    @benchmark
    # each tuple in `arguments` gets applied to each benchmark-method
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

    @benchmark
    def builtin_factorial(self, n):
        return factorial(n)
````

Save it as `factorial.py`, run `testbench factorial`, and we get something like this:

````
================================================================================
Benchmarking Factorial...
================================================================================
For the argument set (5,)
--------------------------------------------------------------------------------
builtin_factorial: min: 0.000000 avg: 0.000001 max: 0.000008
iterative_factorial: min: 0.000001 avg: 0.000002 max: 0.000004
recursive_factorial: min: 0.000001 avg: 0.000002 max: 0.000004
--------------------------------------------------------------------------------
For the argument set (125,)
--------------------------------------------------------------------------------
builtin_factorial: min: 0.000021 avg: 0.000022 max: 0.000025
iterative_factorial: min: 0.000029 avg: 0.000030 max: 0.000045
recursive_factorial: min: 0.000065 avg: 0.000068 max: 0.000198
--------------------------------------------------------------------------------
For the argument set (200,)
--------------------------------------------------------------------------------
builtin_factorial: min: 0.000040 avg: 0.000041 max: 0.000054
iterative_factorial: min: 0.000052 avg: 0.000053 max: 0.000089
recursive_factorial: min: 0.000109 avg: 0.000111 max: 0.000217
--------------------------------------------------------------------------------
````

Run `testbench-color factorial` and we get something much more exciting:

![testbench-color screenshot](https://github.com/startling/testbench/blob/master/testbench_screenshot.png?raw=true)

Those bars indicate how much time it takes, scaled so that the longest time is the widest. Green indicates the fastest trial in the category (categories here are "min", "max", and "avg", and in fact these are just the defaults), red indicates the slowest, and cyan means it's somewhere in the middle.

## To Do

* More solid and strict API -- what do things need to implement to work as benchmarks?
* More configurability in benchmark runners -- group results differently; have smaller, more modular methods.
* real Sphinx API documentation, once this is less of a moving target.
* Dump raw, unfiltered benchmark data to json or similar.
