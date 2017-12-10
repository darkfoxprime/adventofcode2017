#!/usr/bin/env python
# Advent of Code 2017 - http://adventofcode.com/2017
#
# Day 6

class Day6(object):

    def __init__(self, program_input):
        self.program_input = tuple(int(x) for x in program_input.split())

#
# Part 1
#
# The reallocation routine operates in cycles. In each cycle, it finds
# the memory bank with the most blocks (ties won by the lowest-numbered
# memory bank) and redistributes those blocks among the banks. To do
# this, it removes all of the blocks from the selected bank, then moves
# to the next (by index) memory bank and inserts one of the blocks. It
# continues doing this until it runs out of blocks; if it reaches the
# last memory bank, it wraps around to the first one.
#
# The debugger would like to know how many redistributions can be done
# before a blocks-in-banks configuration is produced that has been
# seen before.
#
# My solution:
#   Initialize `cycle` to 0 (the initial condition is cycle #0)
#   Initialize `state` to the program input (as a tuple)
#   Initialize hash `seen` to empty.
#   Loop while `state` is not in `seen`:
#       Store `cycle` in `seen` indexed by `state`
#       Determine the highest `blocks` count in the current state
#           _and_ the `index` of that block count.
#       Determine the reallocation based on the block count
#           reduce(
#                       lambda (lst,blks),slots: (
#                                   lst + [(blks+slots-1)/slots]
#                                 , blks - (blks+slots-1)/slots
#                                 )
#                     , range(slots,0,-1)
#                     , (list(),blocks)
#                   )[0]
#       Subtract `blocks` from the last element of the reallocation
#           array (to handle zeroing out that memory bank first).
#       Take the last `index` + 1 elements of the reallocation array
#           and prepend them to the array.
#       Add each element of the reallaction array to the state array.
#       Increment the `cycle`
#
#   Return `cycle`.
#  (Also return `cycle` minus the `cycle` value stored in `seen` for
#   the current state, since I'm guessing the next part will be to
#   provide the length of the repeating cycle)

    def part1(self):
        cycle = 0
        state = tuple(self.program_input)
        seen = {}
        while state not in seen:
            seen[state] = cycle
#           print "Cycle {0}: State {1!r}".format(cycle, state)
            (blocks, index) = reduce(
                        lambda (maxval,maxidx),idx,state=state:
                                (state[idx],idx) if state[idx] > maxval
                                else (maxval,maxidx)
                      , range(len(state))
                      , (-1,-1)
                    )
            reallocation = reduce(
                        lambda (lst,blks),slots: (
                                    lst + [(blks+slots-1)/slots]
                                  , blks - (blks+slots-1)/slots
                                  )
                      , range(len(state),0,-1)
                      , (list(),blocks)
                    )[0]
            reallocation[-1] -= blocks
            reallocation = reallocation[-(index+1):] + reallocation[:-(index+1)]
            state = tuple(current + reallocated for (current,reallocated) in zip(state, reallocation))
            cycle += 1
#           print "Cycle {0}: Reallocate {1} blocks at index {2}: {3!r}".format(cycle, blocks, index, reallocation)
        return (cycle, cycle - seen[state])

#
# Part 2
#
# Out of curiosity, the debugger would also like to know the size of
# the loop: starting from a state that has already been seen, how many
# block redistribution cycles must be performed before that same state
# is seen again?
#
# My solution:
#   (already solved in part 1)

    def part2(self):
        return None

#
# The puzzle input
#

puzzle_input = '5	1	10	0	1	7	13	14	3	12	8	10	7	12	0	6'

day6 = Day6(puzzle_input)

print 'part 1 solution = {0}'.format( day6.part1() )
print 'part 2 solution = {0}'.format( day6.part2() )
