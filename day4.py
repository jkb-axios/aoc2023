#!/bin/env python3

import sys,os
from pprint import pprint as pp
from pprint import pformat as pf
import numpy

# input is a scratch card per line
# each line starts with "Card 1:" where 1 is the line number
# the rest of each line has space separated "winning numbers", a |, then a list of my numbers


fn='sample.day4'
fn='input.day4'
part1=False
part2= not part1

with open(fn) as f:
    data=f.read()

cards = []
for line in data.splitlines():
    line = line.split(':')[-1]
    winning,mine = line.split('|')
    winning = [int(x) for x in winning.split()]
    mine = [int(x) for x in mine.split()]
    cards.append((winning,mine))
    #print(cards[-1])

if part1:
    points=[]
    for winning,mine in cards:
        wins=set(winning).intersection(mine)
        if len(wins) > 0:
            points.append(2**(len(wins)-1))
        else:
            points.append(0)
    print(f'{sum(points)} points from {points}')

else:
    print('part2')
    card_dict = {i+1:{'cnt':1,'winning':card[0],'mine':card[1]} for i,card in enumerate(cards)}
    total=0
    #pp(card_dict)
    for idx in card_dict:
        card = card_dict[idx]
        winning = card['winning']
        mine = card['mine']
        cnt = card['cnt']
        total = total+cnt
        wins=set(winning).intersection(mine)
        for x in range(len(wins)):
            cpy=card_dict[idx+x+1]
            cpy['cnt'] = cpy['cnt'] + card['cnt']
    print(f'part2 total is {total}')
