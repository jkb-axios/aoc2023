#!/bin/env python3

import sys,os
from pprint import pprint as pp
from pprint import pformat as pf
import numpy

fn='sample.day3'
fn='input.day3'
part1=True
part2= not part1

with open(fn) as f:
    data=f.read()

grid=[]
for line in data.splitlines():
    grid.append([x for x in line])
    #print(''.join(grid[-1]))
#pp(grid)

def isnum(x):
    try:
        return int(x) in range(10)
    except ValueError:
        return False

def issym(x):
    if x == '.' or isnum(x):
        return False
    return True

def is_part_number(symbol_adjacent, row, cols):
    # determine if there is a symbol adjacent to the row/col coords provided
    for col in cols:
        if symbol_adjacent[row][col]:
            return True
    return False

if True:
    parts=[]
    numbers = []
    symbol_adjacent = [[False]*len(grid[0]) for _ in grid]
    gears=[]
    for row,line in enumerate(grid):
        cur_num = []
        num_cols = []
        for col,val in enumerate(line):
            if isnum(val):
                cur_num.append(val)
                num_cols.append(col)
            else:
                if val == '*':
                    gears.append({'row':row,'col':col})
                if cur_num:
                    num = int(''.join(cur_num))
                    numbers.append({'num':num, 'row':row, 'cols':num_cols})
                    # if is_part_number(symbol_adjacent, row, num_cols):
                    #     parts.append(num)
                    # then when done
                    cur_num = []
                    num_cols = []
                if issym(val):
                    symbol_adjacent[row][col]=True
                    min_row = row
                    max_row = row
                    min_col = col
                    max_col = col
                    if row > 0:
                        min_row = row-1
                    if col < len(grid[0])-1:
                        max_col = col+1
                    if col > 0:
                        min_col = col-1
                    if row < len(grid)-1:
                        max_row = row+1
                    for r in range(min_row,max_row+1):
                        for c in range(min_col,max_col+1):
                            symbol_adjacent[r][c]=True
        if cur_num:
            num = int(''.join(cur_num))
            numbers.append({'num':num, 'row':row, 'cols':num_cols})
    for n_dict in numbers:
        if is_part_number(symbol_adjacent, n_dict['row'], n_dict['cols']):
            parts.append(n_dict['num'])
        # else:
        #     print(f'NOT A PART: {n_dict}')
    print(f'sum: {sum(parts)} parts: {parts}')

    #530495 <-- PART 1 answer

    # part 2 code...
    def find_adjacent_numbers(numbers, row, col):
        nums=[]
        for num in numbers:
            for numcol in num['cols']:
                if abs(row-num['row']) <=1 and abs(col-numcol) <= 1:
                    nums.append(num['num'])
                    break
        return nums

    total=0
    for gear in gears:
        r = gear['row']
        c = gear['col']
        nums = find_adjacent_numbers(numbers, r, c)
        if len(nums) == 2:
            ratio = nums[0]*nums[1]
            total = total+ratio
    print(f'part2 total is {total}')





else:
    pass