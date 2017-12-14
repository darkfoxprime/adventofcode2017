#!/usr/bin/env python
# Advent of Code 2017 - http://adventofcode.com/2017
#
# Day 13

import sys

import re
import time
import fractions

class Day13(object):

    def __init__(self, program_input):
        # transform the input, of the form
        #    <depth>: <range>
        # to a dict mapping depth to range.
        re_depthrange = re.compile(r'^ *(\d+) *: *(\d+) *$')
        self.program_input = dict(
                    (int(dr[0]), int(dr[1]))
                    for dr in (
                        re_depthrange.match(line).groups()
                        for line in program_input.split('\n')
                        if line
                    )
                )

#
# Part 1
#
# The program input represents scanners at various 'depths'
# that move back and forth in their range: they start at position
# 0, move up to <range>-1, then back down to 0.
#
# Find the number of scanners who will be at position 0 at time <depth>.
# Return the sum of those scanners' <depth> * <range>
#
# My solution:
#   Return the sum of <depth> * <range> for each scanner for whom
#   depth % (2*(range-1)) == 0

    def part1(self):
        return sum(
                    depth * range
                    for (depth,range) in self.program_input.items()
                    if depth % (2 * (range-1)) == 0
                )

#
# Part 2
#
# Find how long you need to delay in order for the number of scanners
# for whom (delay+depth) % (2*(range-1)) == 0 to be 0.
#
# My solution:
#    Brute force:  Increment `delay` until the list is size 0.
#
# There has to be a mathematical solution to this
# But I can't figure it out right now 
#
# Redefine scanner as (depth, cycle) where cycle = 2*(range-1)
#
# The maximum delay is the least_common_multiple of all scanner `cycle` values.
#
# find delay such that
#    (delay+depth) is not an element of { i*cycle : 0 <= i*cycle < max_delay }
#    -or-
#    delay is not an element of { i*cycle-depth : 0 <= i*cycle-depth < max_delay }
#    for all (depth,range) value pairs in the set of scanners.
#   
# My solution:
#   Transform scanner dict into list of (depth,cycle)
#   use `fractions.gcd` in a reduce to find the least_common_multiple
#       reduce(lambda a,b:(a*b)/fractions.gcd(a,b), (2,3,4,6), 1)
#   start with an empty set
#   for each scanner, union the set of range((cycle-(depth%cycle))%cycle, least_common_multiple, cycle)
#   after all scanners are in the union, take the difference of that and the set of range(least_common_multiple)
#   the lowest number left in the set is the delay
#
# Each scanner is blocked at time (depth%cycle) + i*cycle for any non-negative integer i

    def part2_bruteforce(self):
        delay = 0
        # optimization: convert scanners dict to list of (period, depth)
        scanners = sorted((2*(range-1), depth) for (depth, range) in self.program_input.items())
        while reduce(
                    lambda blocked,(period,depth),delay=delay:
                        blocked or (delay+depth) % period == 0
                  , scanners
                  , False
                ):
            delay += 1
        return delay

#
# The puzzle input
#

puzzle_input = '''
0: 5
1: 2
2: 3
4: 4
6: 6
8: 4
10: 8
12: 6
14: 6
16: 14
18: 6
20: 8
22: 8
24: 10
26: 8
28: 8
30: 10
32: 8
34: 12
36: 9
38: 20
40: 12
42: 12
44: 12
46: 12
48: 12
50: 12
52: 12
54: 12
56: 14
58: 14
60: 14
62: 20
64: 14
66: 14
70: 14
72: 14
74: 14
76: 14
78: 14
80: 12
90: 30
92: 17
94: 18
'''

day13 = Day13(puzzle_input)

print 'part 1 solution = {0}'.format( day13.part1() )

t = time.time()
s = day13.part2_bruteforce()
t = time.time() - t
print 'part 2 solution = brute force {0} time {1}'.format( s, t )

