#!/usr/bin/env python
# Advent of Code 2017 - http://adventofcode.com/2017
#
# Day 14

# uses day10!
import day10

class Day14(object):

    def __init__(self, program_input):
        self.program_input = program_input

#
# Part 1
#
# Given a key sequence, calculate the number of `1` bits in
# the series of knot hashes <key>-0, <key>-1, ..., <key>-127
#
# My solution:
#   for each number from 0 to 127,
#       calculate the knot hash, convert it to an integer,
#       convert it to a binary string, strip the leading '0b',
#       replace all '0' characters with '', and find the length
#       of the resulting string.
#   sum the results.

    def part1(self):
        return sum(
                    len(
                        (
                            bin(
                                int(
                                    day10.Day10(
                                        '{0}-{1}'.format(self.program_input, seq)
                                    ).part2()
                                  , 16
                                )
                            )[2:]
                        ).replace('0', '')
                    )
                    for seq in range(128)
                )

#
# Part 2
#
# Given a key sequence, convert that key sequence into a
# series of knot hashes <key>-0, <key>-1, ..., <key>-127 .
# Find the number of contiguous groups of `1` bits when
# viewing the sequence as a 2-dimensional bit array.
#
# My solution:
#   Initialize `grid` to an empty list
#   For each knot hash,
#     for each position in the hash,
#       If the bit in this position is `0`,
#         Add `None` to `grid`
#       Otherwise add the number `0` to `grid`
#   Initialize `group` to 0
#   For each (x,y) position in the grid
#     If `grid` at this position is `0`,
#       Increment `group`
#       Set `check` list to [(x,y)]
#       while `check` is not empty,
#         pop (x,y) off `check`
#         if `grid` at this position is `0`,
#           replace `grid` at this position with `group`
#           if x < 127, push (x+1,y) into `check`
#           if x > 0,   push (x-1,y) into `check`
#           if y < 127, push (x,y+1) into `check`
#           if y > 0,   push (x,y-1) into `check`
#   Return `group`

    def part2(self):
        grid = []
        for seq in range(128):
            hash = (
                        bin(
                            int('1' +
                                day10.Day10(
                                    '{0}-{1}'.format(self.program_input, seq)
                                ).part2()
                              , 16
                            )
                        )[3:]
                    )
            for bit in hash:
                grid.append(
                    None if bit == '0'
                        else 0
                )
        group = 0
        for y in range(128):
            for x in range(128):
                if grid[y*128+x] == 0:
                    group += 1
                    check = [(x,y)]
                    while len(check) > 0:
                        (xx,yy) = check.pop()
                        if grid[yy*128+xx] == 0:
                            grid[yy*128+xx] = group
                            if xx < 127: check.append((xx+1,yy))
                            if xx >   0: check.append((xx-1,yy))
                            if yy < 127: check.append((xx,yy+1))
                            if yy >   0: check.append((xx,yy-1))
        return group

#
# The puzzle input
#

puzzle_input = 'jzgqcdpd'

sample_input = 'flqrgnkx'

day14 = Day14(puzzle_input)

print 'part 1 solution = {0}'.format( day14.part1() )
print 'part 2 solution = {0}'.format( day14.part2() )
