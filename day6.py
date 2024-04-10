#!/bin/env python3

import sys,os
from pprint import pprint as pp
from pprint import pformat as pf
import numpy

# start speed is 0 mm/ms
speed=0 # mm/ms

# speed increase per ms button hold is 1 mm/ms
incr=1 # mm/ms

fn='sample.day6'
fn='input.day6'
part1=False
part2= not part1

with open(fn) as f:
    data=f.read()

race_times,race_distance = data.splitlines()
if part1:
    race_times = [int(x) for x in race_times.split()[1:]]
    race_distance = [int(x) for x in race_distance.split()[1:]]
    race_info = zip(race_times,race_distance)
    # race_info has an entry for each race
    # each entry is a tuple of race_time (ms), race_distance (mm)
    # race distance is the record to beat
else:
    race_times = [int(''.join(race_times.split()[1:]))]
    race_distance = [int(''.join(race_distance.split()[1:]))]
    race_info = zip(race_times,race_distance)

pp(race_times)
pp(race_distance)
#pp([(x,y) for x,y in race_info])

def calc_distance(t_button, t_race):
    s=t_button
    d=(t_race-t_button)*s
    return d

wins=[]
for t_race, record in race_info:
    #print(t_race, record)
    w=0
    for t_button in range(t_race):
        d=calc_distance(t_button,t_race)
        if d > record:
            w=w+1
        elif w > 0:
            break
    wins.append(w)
print(f'wins {wins} product {numpy.prod(wins)}')