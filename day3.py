#!/usr/bin/env python
# Advent of Code 2017 - http://adventofcode.com/2017
#
# Day 3

import math

class Day3(object):

    def __init__(self, puzzle_input):
        self.puzzle_input = puzzle_input

#
# Part 1
#
# On a grid that is addressed in a spiral pattern as shown here...
#
# 17  16  15  14  13
# 18   5   4   3  12
# 19   6   1   2  11
# 20   7   8   9  10
# 21  22  23---> ...
#
# Identify the Manhattan Distance between the puzzle_input and
# square `1`.
#
# My solution:
#   First, identify the `ring` number which contains the puzzle input.
#     Square `1` is in ring `0`; squares `2` through `9` are in ring `1`, etc.
#     The ring number is:
#       ceil( (-4 + 4*sqrt(puzzle_input) )/8 )
#   Second, identify the `size` of the ring - the number of squares on each side.
#     For ring 0, this is 1.
#     For any other ring, this is `ring` times 2.
#     So, the `size` is:
#       1 if ring == 0 else 2*ring
#     Or
#       min(1, 2*ring)
#   Third, identify the `first` square of the ring:
#     For ring 0, this is 1.
#     For any other ring, this is 2 + 4*ring*(ring-1)
#     So, `first` is:
#       1 if ring == 0 else 2+4*ring*(ring-1)
#   Fourth, optionally, identify the `rotation` of the puzzle input:
#     Not needed for this part of the puzzle, but will be needed if we 
#     are required to generate the path.
#     I am defining the `rotation` of a square as being the number of
#     clockwise rotations needed to cause that square to be on the
#     "right" edge of the ring.
#     The rotation of a square is the integral quotient of the square's
#     address, minus the `first` square of the ring, divided by the
#     `size` of the ring.
#     So, the `rotation` is:
#       (puzzle_input - first) / size
#     Or, expanded out:
#       (puzzle_input - (1 if ring == 0 else 2+4*ring*(ring-1))) /
#         (1 if ring == 0 else 2*ring)
#     Or, simplified (since ring 0 is always rotation 0):
#       0 if ring == 0 else
#         (puzzle_input - 2 - 4*ring*(ring-1)) / (2*ring)
#   Fifth, identify the vertical `offset` between square `1` and the
#     first square of the ring.
#     For ring 0, this is 0.
#     For any other ring, this is `ring` - 1.
#     So, `offset` is:
#       0 if ring == 0 else ring-1
#     Or
#       min(0, ring-1)
#   Finally, calculate the manhattan `distance` between the puzzle input
#   and square `1`.
#     This is the ring number, plus the absolute value of
#       the modulo of
#         the puzzle_input minus the `first` square of the ring
#         with respect to the ring `size`
#        minus the `offset`
#     Thus, the `distance` is
#       ring + abs( (puzzle_input - first) % size - offset )
#     To simplify the expansions, we special-case square `1` (ring `0`):
#       0 if puzzle_input == 1 else
#         ring + abs( (puzzle_input - first) % size - offset )
#     Expanding the second part:
#       0 if puzzle_input == 1 else
#         ring + abs( (puzzle_input - (2+4*ring*(ring-1))) % (2*ring) - (ring-1) )
#       0 if puzzle_input == 1 else
#         ring + abs( (puzzle_input - 2 - 4*ring*(ring-1)) % (2*ring) - (ring-1) )
#     Expanding `ring` completely:
#       0 if puzzle_input == 1 else
#         ceil( (-4 + 4*sqrt(puzzle_input) )/8 ) + abs( (puzzle_input - 2 - 4*ceil( (-4 + 4*sqrt(puzzle_input) )/8 )*(ceil( (-4 + 4*sqrt(puzzle_input) )/8 )-1)) % (2*ceil( (-4 + 4*sqrt(puzzle_input) )/8 )) - (ceil( (-4 + 4*sqrt(puzzle_input) )/8 )-1) )

    def ring(self, square):
        return int(math.ceil( (-4 + 4*math.sqrt(square) )/8 ))

    def size(self, ring):
        return 1 if ring == 0 else 2*ring

    def first(self, ring):
        return 1 if ring == 0 else 2+4*ring*(ring-1)

    def rotation(self, square, ring):
        return 0 if square == 1 else (
                    (square - 2 - 4*ring*(ring-1)) / (2*ring)
                )

    def offset(self, ring):
        return 0 if ring == 0 else ring-1

    def part1_imperative(self):
        if self.puzzle_input == 1:
            return 0
        else:
            ring = self.ring(self.puzzle_input)
            size = self.size(ring)
            first = self.first(ring)
            offset = self.offset(ring)
            return ring + abs( (self.puzzle_input - first) % size - offset )

    def part1_functional(self):
        return 0 if self.puzzle_input == 1 else int(
                    math.ceil( (-4 + 4*math.sqrt(self.puzzle_input) )/8 ) +
                    abs(
                        (self.puzzle_input - 2 - 4*math.ceil( (-4 + 4*math.sqrt(self.puzzle_input) )/8 )*(math.ceil( (-4 + 4*math.sqrt(self.puzzle_input) )/8 )-1)) % (2*math.ceil( (-4 + 4*math.sqrt(self.puzzle_input) )/8 )) - (math.ceil( (-4 + 4*math.sqrt(self.puzzle_input) )/8 )-1)
                    )
                )

#
# Part 2
#
# As a stress test on the system, the programs here clear the grid
# and then store the value 1 in square 1. Then, in the same allocation
# order as shown above, they store the sum of the values in all adjacent
# squares, including diagonals.
#
# What is the first value written that is larger than your puzzle input?
#
# My solution:
#   Brute force:
#     Use a hash to record each stored value keyed on the (x,y) position
#     the memory grid.
#     Initialize the hash with { (0,0): 1 }
#     Initialize (x,y) with (0,0), `ring` with 0, and (dx,dy) with (1,0)
#     Loop until the last stored value is > puzzle_input:
#       Increment (x,y) by (dx,dy)
#       if abs(x)>ring or abs(y)>ring:
#         if (dx,dy) == (1,0), increment ring.
#         Replace (dx,dy) with (dy,-dx)
#       For all eight neighbors of (x,y), sum the hash contents of those
#       grid positions; store the resulting sum as (x,y).
#     Return the last stored value

    def part2(self):
        values = { (0,0): 1 }
        (x,y) = (0,0)
        (dx,dy) = (1,0)
        ring = 0
        while values[(x,y)] <= self.puzzle_input:
            if abs(x) == ring and abs(y) == ring:
                if (dx,dy) != (1,0): (dx,dy) = (dy,-dx)
            (x,y) = (x+dx, y+dy)
            if abs(x) > ring or abs(y) > ring:
                ring += 1
                (dx,dy) = (dy,-dx)
            values[(x,y)] = sum(
                        values[(xx,yy)]
                        for xx in (x-1,x,x+1)
                        for yy in (y-1,y,y+1)
                        if (xx,yy) in values
                    )
            print "values[{0!r}]={1!r}".format( (x,y), values[(x,y)] )
        return values[(x,y)]

#
# The puzzle input
#

puzzle_input = 277678

day3 = Day3(puzzle_input)

print 'part 1 imperative solution = {0}'.format( day3.part1_imperative() )
print 'part 1 functional solution = {0}'.format( day3.part1_functional() )
print 'part 2 solution = {0}'.format( day3.part2() )
