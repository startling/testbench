#!/usr/bin/env python
# -*- coding: utf-8 -*-


def avg(iterable):
    "A generic `average` function that works on any iterable, including iterators."
    total = float(0)
    count = float(0)
    for n in iterable:
        total += n
        count += 1
    return total/count
