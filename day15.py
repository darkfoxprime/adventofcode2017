#!/usr/bin/env python
# Advent of Code 2017 - http://adventofcode.com/2017
#
# Day 15

class Day15(object):

    @staticmethod
    def generator(factor, startingvalue, zerobits=0):
        if zerobits == 0:
            check = lambda x:True
        else:
            check = lambda x,m=0xFFFFFFFF >> (32 - zerobits): x&m == 0
        while True:
            startingvalue = (startingvalue * factor) % 0x7FFFFFFF
            if check(startingvalue):
                yield startingvalue

    def __init__(self, program_input):
        self.program_input = program_input

#
# Part 1
#
# (Problem Description)
#
# My solution:
#   (Pseudocode)

    def part1(self):
        gen1 = Day15.generator(16807, self.program_input[0])
        gen2 = Day15.generator(48271, self.program_input[1])
        count = 40000000
        matches = 0
        while count > 0:
          count -= 1
          val1 = gen1.next() & 0xFFFF
          val2 = gen2.next() & 0xFFFF
          if val1 == val2:
              matches += 1
        return matches

#
# Part 2
#
# (Problem Description)
#
# My solution:
#   (Pseudocode)

    def part2(self):
        gen1 = Day15.generator(16807, self.program_input[0], 2)
        gen2 = Day15.generator(48271, self.program_input[1], 3)
        count = 5000000
        matches = 0
        while count > 0:
          count -= 1
          val1 = gen1.next() & 0xFFFF
          val2 = gen2.next() & 0xFFFF
          if val1 == val2:
              matches += 1
        return matches

#
# The puzzle input
#

puzzle_input = (516, 190)
test_input = (65, 8921)

day15 = Day15(puzzle_input)

print 'part 1 solution = {0}'.format( day15.part1() )
print 'part 2 solution = {0}'.format( day15.part2() )
