#!/bin/env python3

import sys,os
from pprint import pprint as pp
from pprint import pformat as pf
import numpy

fn='sample.day2'
fn='input.day2'
part1=False
part2= not part1

with open(fn) as f:
    data=f.read()

# input is a game per line
# each line starts with "Game 1:" where 1 is the line number
# the rest of the line is a series of "sets" separated by a semi-colon
# each set is a comma-separated list of "cubes"
# a "cube" is a number and a color: i.e. "3 blue"
games = []
games_dict = {}
for game in data.splitlines():
    game = game.split(':')[-1]
    sets = game.split(';')
    game_dict = {}
    game_dict['sets']=[]
    for s in sets:
        s_dict = {}
        for cube in s.split(','):
            num,color = cube.split()
            s_dict[color]=int(num)
        game_dict['sets'].append(s_dict)
    games.append(game_dict)
    games_dict[len(games)] = game_dict

#pp(games_dict)

if part1:
    # bag only contains: 12 red, 13 green, 14 blue
    # which games are possible?
    # answer is the sum of the possible game id's
    bag={
        'red':12,
        'green':13,
        'blue':14
    }
    possible_ids = []
    for gid, game in games_dict.items():
        #print(f"{gid}: {game}")
        possible=True
        for s in game['sets']:
            for color in s:
                if s[color] > bag[color]:
                    possible=False
                    break
            if not possible:
                break
        if possible:
            possible_ids.append(gid)
    print(f'sum: {sum(possible_ids)} possible games: {possible_ids}')

else:
    print('part2')
    powers = []
    for gid, game in games_dict.items():
        colors={}
        for s in game['sets']:
            for color in s:
                if color not in colors:
                    colors[color]=s[color]
                elif colors[color] < s[color]:
                    colors[color]=s[color]
        power = colors.get('red',0)*colors.get('green',0)*colors.get('blue',0)
        powers.append(power)
    print(f'sum: {sum(powers)} powers: {powers}')
