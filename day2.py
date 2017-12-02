#!/usr/bin/env python
# Advent of Code 2017 - http://adventofcode.com/2017
#
# Day 2

class Day2(object):

    def __init__(self, program_input):
        # process the input into an array of arrays of numbers
        #   Split rows around newlines;
        #   for each such line that is not empty:
        #     split columns around whitespace;
        #     convert each column to an integer.
        self.program_input = [
                    [int(col) for col in row]
                    for row in (
                        row.split()
                        for row in program_input.split('\n')
                    )
                    if len(row) > 0
                ]

#
# Part 1
#
# For each row, determine the difference between the largest value and
# the smallest value; the checksum is the sum of all of these differences.
#
# My solution:
#   For each row, sort the row;
#       calculate the difference between the last and first value;
#       and sum those differences.

    def part1(self):
        return sum(
                    row[-1] - row[0]
                    for row in (
                        sorted(row)
                        for row in self.program_input
                    )
                )

#
# Part 2
#
# The goal is to find the only two numbers in each row where one evenly
# divides the other - that is, where the result of the division operation
# is a whole number. They would like you to find those numbers on each
# line, divide them, and add up each line's result.
#
# My map/reduce solution:
#   For each row, sort the row;
#       reduce the row to the quotient as described below;
#       and return the checksum of all the row quotients.
#   To reduce the row to a quotient, use an initializer of (None,row[1:])
#   for a lambda that takes (quotient,checkvalues),denominator;
#       if `quotient` is not None, return (quotient,[]);
#       otherwise return the quotient found in `checkvalues`:
#       run a new reduction over `checkvalues` with an initializer of (None,denominator)
#       for a lambda that takes (quotient,denominator),numerator;
#           if `quotient` is not None, return (quotient,denominator)
#           otherwise if numerator % denominator == 0, return (numerator/denominator,numerator)
#           otherwise return (None,denominator)
#       The new quotient is the [0] indexed value of the lambda's return.

    def part2_map_reduce(self):
        return sum(
                    reduce(
                        lambda (quotient,checkvalues),denominator:
                            (quotient,[]) if quotient is not None
                            else (reduce(
                                lambda (quotient,denominator),numerator:
                                    (quotient,denominator) if quotient is not None
                                    else
                                        (numerator/denominator, numerator)
                                            if numerator % denominator == 0
                                        else
                                            (None, denominator)
                              , checkvalues
                              , (None, denominator)
                            )[0], checkvalues[1:])
                          , row
                          , (None, row[1:])
                    )[0]
                    for row in (
                        sorted(row)
                        for row in self.program_input
                    )
                )

# My imperative solution:
#    Initialize the sum to 0
#    For each row, sort the row.
#        While the row has at least two elements,
#            set the denominator to row[0]
#            set the row to row[1:]
#            for each numerator in the row,
#                if numerator % denominator == 0,
#                    add (numerator / denominator) to sum
#                    empty the row
#                    break out of the numerator loop

    def part2_imperative(self):
        sum = 0
        for row in self.program_input:
            row = sorted(row)
            while len(row) > 1:
                denominator = row.pop(0)
                for numerator in row:
                    if numerator % denominator == 0:
                        sum += numerator / denominator
                        row = []
                        break
        return sum

#
# The puzzle input
#

puzzle_input = '''
1919\t2959\t82\t507\t3219\t239\t3494\t1440\t3107\t259\t3544\t683\t207\t562\t276\t2963
587\t878\t229\t2465\t2575\t1367\t2017\t154\t152\t157\t2420\t2480\t138\t2512\t2605\t876
744\t6916\t1853\t1044\t2831\t4797\t213\t4874\t187\t6051\t6086\t7768\t5571\t6203\t247\t285
1210\t1207\t1130\t116\t1141\t563\t1056\t155\t227\t1085\t697\t735\t192\t1236\t1065\t156
682\t883\t187\t307\t269\t673\t290\t693\t199\t132\t505\t206\t231\t200\t760\t612
1520\t95\t1664\t1256\t685\t1446\t253\t88\t92\t313\t754\t1402\t734\t716\t342\t107
146\t1169\t159\t3045\t163\t3192\t1543\t312\t161\t3504\t3346\t3231\t771\t3430\t3355\t3537
177\t2129\t3507\t3635\t2588\t3735\t3130\t980\t324\t266\t1130\t3753\t175\t229\t517\t3893
4532\t164\t191\t5169\t4960\t3349\t3784\t3130\t5348\t5036\t2110\t151\t5356\t193\t1380\t3580
2544\t3199\t3284\t3009\t3400\t953\t3344\t3513\t102\t1532\t161\t143\t2172\t2845\t136\t2092
194\t5189\t3610\t4019\t210\t256\t5178\t4485\t5815\t5329\t5457\t248\t5204\t4863\t5880\t3754
3140\t4431\t4534\t4782\t3043\t209\t216\t5209\t174\t161\t3313\t5046\t1160\t160\t4036\t111
2533\t140\t4383\t1581\t139\t141\t2151\t2104\t2753\t4524\t4712\t866\t3338\t2189\t116\t4677
1240\t45\t254\t1008\t1186\t306\t633\t1232\t1457\t808\t248\t1166\t775\t1418\t1175\t287
851\t132\t939\t1563\t539\t1351\t1147\t117\t1484\t100\t123\t490\t152\t798\t1476\t543
1158\t2832\t697\t113\t121\t397\t1508\t118\t2181\t2122\t809\t2917\t134\t2824\t3154\t2791
'''


day2 = Day2(puzzle_input)

print 'part 1 solution = {0}'.format( day2.part1() )
print 'part 2 map/reduce solution = {0}'.format( day2.part2_map_reduce() )
print 'part 2 imperative solution = {0}'.format( day2.part2_imperative() )
