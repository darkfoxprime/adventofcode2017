#!/usr/bin/env python
# Advent of Code 2017 - http://adventofcode.com/2017
#
# Day 10

class Day10(object):

    def __init__(self, program_input):
        self.program_input = program_input

#
# Part 1
#
# Start with a list containing the sequence from 0 to 255,
# a current position of 0, and a skip size of 0.
# For each length in the program input, reverse that many
# items in the list beginning at the current position
# (wrapping around as needed).  Then move the current
# position forward by the length plus the skip size
# (again, wrapping around as needed).  Finally,
# increment the skips ize
#
# My solution:
#   Initialize `lst`, `pos`, and `skp` as specified.
#   For each length in the list:
#       Reverse the first `length` items in `lst`
#       Rotate the first `(length+skp)%256` items to the end of `lst`
#       set `pos` to `(pos+lst+skp)%256`
#       increment `skp`
#   Return lst[0-pos] * lst[1-pos]

    def part1(self):
        lst = range(256)
        pos = 0
        skp = 0
        for length in (int(x) for x in self.program_input.split(',')):
            for i in range(length/2):
                (lst[i], lst[length-i-1]) = (lst[length-i-1], lst[i])
            lst = lst[(length+skp)%256:] + lst[:(length+skp)%256]
            pos = (pos + length + skp) % 256
            skp += 1
        return lst[0-pos] * lst[1-pos]

#
# Part 2
#
# program input should be treated as a sequence of bytes, each byte
# being one length.
# Add standard suffix [17,31,73,47,23] to end of length sequence.
# Run 64 rounds of reverses, maintaining `pos` and `skp` between
# rounds.
# Then condense the list by a factor of 16 by xor'ing all numbers
# in each block of 16 values.
# Finally, convert the list to hex.
#
# My solution:
#   Same initial solution as part 1, changing program input treatment
#       to using `ord` to obtain values and appending standard suffix.
#   Run the `for` loop from part 1 64 times.
#   Rotate the list by `-pos`.
#   initialize `hsh` to an empty string.
#   while the list is not empty:
#       reduce the first 16 elements of list by using the `xor` operator
#       Add the 2-digit hex representation of the result of that reduction to `hsh`
#       Remove the first 16 elements of list
#   return the hash

    def part2(self):
        lst = range(256)
        pos = 0
        skp = 0
        for round in xrange(64):
            for length in (ord(x) for x in self.program_input + '\x11\x1F\x49\x2F\x17'):
                for i in range(length/2):
                    (lst[i], lst[length-i-1]) = (lst[length-i-1], lst[i])
                lst = lst[(length+skp)%256:] + lst[:(length+skp)%256]
                pos = (pos + length + skp) % 256
                skp += 1
        lst = lst[-pos:] + lst[:-pos]
        hsh = ''
        while len(lst) > 0:
            hsh += hex(256 + reduce(lambda a,b:a^b, lst[:16]))[-2:]
            lst = lst[16:]
        return hsh

if __name__ == '__main__':

    #
    # The puzzle input
    #

    puzzle_input = '227,169,3,166,246,201,0,47,1,255,2,254,96,3,97,144'

    day10 = Day10(puzzle_input)

    print 'part 1 solution = {0}'.format( day10.part1() )
    print 'part 2 solution = {0}'.format( day10.part2() )
