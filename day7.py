#!/bin/env python3

import sys,os
from pprint import pprint as pp
from pprint import pformat as pf
import numpy

fn='sample.day7'
fn='input.day7'
part1=False
part2= not part1

with open(fn) as f:
    data=f.read()

# hands:
# - 5 of a kind
# - 4 of a kind
# - full house
# - 3 of a kind
# - two pair
# - one pair
# - high card
# FOR TIES - higher "first card" wins, then 2nd, 3rd, 4th, 5th until a winner is found
# i.e. 33332 and 2AAAA are both four of a kind hands, but 33332 is stronger because its first card is stronger

# bids and rank:
# - winning hand wins the bid amount multiplied by its rank
# - rank is 1 for weakest hand, 2 for 2nd weakest, etc

# INPUT is a hand and bid per line: a hand is 5 cards, then a space, and the bid is a number

# order hands on strength to assign ranks
# calculate winnings for each hand (rank * bid)
# sum of winnings is the answer

cards1 = '23456789TJQKA'
cards2 = 'J23456789TQKA'
cards = cards1 if part1 else cards2

class Hand:
    cards = cards
    strengths = 'H123F45' # H(igh card), 1(pair), 2(pair), 3(of a kind), F(ull house), 4(of a kind), 5(of a kind)
    def __init__(self, hand, bid=1):
        self.hand=hand
        self.bid=bid
        self.value = get_hand_value(self)
    def __repr__(self):
        return f'Hand({self.hand}[{self.value}],{self.bid})'
    # def comp(self, h2): # h2 is of class Hand
    #     return comp_hands(self,h2)

# cards = Hand.cards #'23456789TJQKA'
# strengths = Hand.strengths #'H123F45' # H(igh card), 1(pair), 2(pair), 3(of a kind), F(ull house), 4(of a kind), 5(of a kind)
# card_map = {c:i+2 for i,c in enumerate(cards)}
# strength_map = {s:i for i,s in enumerate(strengths)} # values are arbitrary really, all that matters is order

# def comp_cards(c1,c2):
#     ''' use this method like:
#             if comp_cards(c1,c2) > 0:
#         to be the same as:
#             if c1 > c2:
#         or for equality, if c1==c2 works just fine instead of this method
#     '''
#     return Hand.cards.index(c1) - Hand.cards.index(c2)

# def comp_strengths(s1,s2):
#     ''' use this method like:
#             if comp_strengths(s1,s2) > 0:
#         to be the same as:
#             if s1 > s2:
#         or for equality, if s1==s2 works just fine instead of this method
#     '''
#     return Hand.strengths.index(s1) - Hand.strengths.index(s2)

# def comp_hands(h1,h2): # expect h1,h2 to be of class Hand
#     cs = comp_strengths(h1.strength_value,h2.strength_value)
#     if cs != 0:
#         return cs
#     for i in range(5):
#         cc = comp_cards(h1.hand[i],h2.hand[i])
#         if cc != 0:
#             return cc
#     return 0

def get_hand_strength(hand):
    same1=0
    same2=0
    done=[]
    jokers=0
    for card in hand.hand:
        if card in done:
            continue
        done.append(card)
        cnt=hand.hand.count(card)
        if part2 and card == 'J': # part 2 only
            jokers = cnt
            continue
        if cnt > same1:
            same2=same1
            same1=cnt
        elif cnt > same2:
            same2=cnt
    # now apply jokers if part2
    if part2:
        same1 = same1 + jokers
    if same1 > 3:
        return str(same1) # 5 or 4 of a kind
    elif same1 == 3:
        if same2 == 2:
            return 'F' # full house
        return '3' # 3 of a kind
    elif same1 == 2:
        if same2 == 2:
            return '2' # 2 pair
        return '1' # 1 pair
    return 'H' # high card

def get_strength_value(s):
    return Hand.strengths.index(s) * 1e10

def get_hand_strength_value(hand):
    return get_strength_value(get_hand_strength(hand))

def get_hand_value(hand):
    val=get_hand_strength_value(hand)
    e = 8
    for c in hand.hand:
        val = val + Hand.cards.index(c) * 10**e
        e = e-2
    return val

myhands = []
for line in data.splitlines():
    c,b = line.split()
    myhands.append(Hand(c,int(b)))
sorted_hands = sorted(myhands,key=lambda x: x.value)
winnings = [(i+1)*h.bid for i,h in enumerate(sorted_hands)]
total = sum(winnings)

# first attempt:  250195639 is TOO HIGH
# second attempt: 250058342 is correct
# part 2 answer is 250506580