#!/bin/env python3

import sys
from pprint import pprint as pp
from pprint import pformat as pf

class mymap:
    def __init__(self,line=None, mm=None):
        self.maps={}
        self.rmaps={}
        if line:
            line = line.split()[0]
            k1,k2 = line.split('-to-')
            self.k1=k1
            self.k2=k2
        elif mm:
            self.k1=mm.k1
            self.k2=mm.k2
            self.maps.update(mm.maps)
            self.rmaps.update(mm.rmaps)
        else:
            raise ValueError('Must specify either line or mm (line takes precedence)')
    def add_line(self,line):
        r2,r1,num=[int(x) for x in line.split()]
        self.maps[r1] = (r1+num-1,r2-r1) # first=last,offset
        self.rmaps[r2] = (r2+num-1,r1-r2) # first=last,offset
    def get(self,n1):
        for m in self.maps:
            if n1 >= m and n1 <= self.maps[m][0]:
                return n1+self.maps[m][1]
        return n1
    def rget(self,n2):
        for m in self.rmaps:
            if n2 >= m and n2 <= self.rmaps[m][0]:
                return n2+self.rmaps[m][1]
        return n2
    def __repr__(self):
        return f"mymap({self.k1}-to-{self.k2}):\n{pf(self.maps, indent=4)}\n{pf(self.rmaps, indent=4)}"

def parse_seeds(line):
    seeds=[]
    vals = [int(x) for x in line.split()]
    for i in range(int(len(vals)/2)):
        seeds.append(range(vals[i*2],vals[i*2]+vals[i*2+1]))
    return seeds

def create_mapping(d):
    seeds=None
    mapping={}
    rmapping={}
    k=None
    for line in d.splitlines():
        if line.startswith('seeds:'):
            line=line.split('seeds:')[-1]
            # part 1:
            #seeds={int(x):{} for x in line.split()}
            seeds1=[int(x) for x in line.split()]
            # part 2:
            seeds2=parse_seeds(line)
            seeds=(seeds1,seeds2) # return seeds for part 1 and part 2
            continue
        elif 'map' in line:
            #process_seeds(k, mapping, seeds) # part 1 only
            mm=mymap(line)
            mapping[mm.k1]=mm
            rmapping[mm.k2]=mm
            k=mm.k1
            continue
        elif k is None:
            continue
        elif len(line.split()) == 3:
            mapping[k].add_line(line)
            # TODO nothing to do with rmapping, right?
    #process_seeds(k, mapping, seeds) # part 1 only
    return seeds,mapping,rmapping

def process_seeds(k1, mapping, seeds):
    if k1 is None:
        return
    mm=mapping[k1]
    k2 = mm.k2
    for seed in seeds:
        k1val = seeds[seed].get(k1,seed)
        k2val=mm.get(k1val)
        seeds[seed][k2]=k2val

def common(fn):
    with open(fn) as f:
        data=f.read()
    seeds,mapping,rmapping = create_mapping(data)
    return seeds,mapping,rmapping

def get_loc(seed,mapping):
    k='seed'
    val=seed
    while True:
        try:
            m=mapping[k]
        except KeyError:
            return val
        k=m.k2
        val = m.get(val)

def get_seed(loc,rmapping):
    k='location'
    val=loc
    while True:
        try:
            m=rmapping[k]
        except KeyError:
            return val
        k=m.k1
        val = m.rget(val)

def solve1(seeds, mapping):
    loc=None
    locseed=None
    part=2
    try:
        for s in seeds:
            try:
                len(s)
            except TypeError:
                s = [s]
                part=1
            for seed in s:
                l = get_loc(seed,mapping)
                if loc is None or l < loc:
                    loc = l
                    locseed = seed
    except KeyboardInterrupt:
        print(f'Caught ctrl+C')
        print(f'seed {seed} and s {s}')
    print(f'meth1.part{part}:lowest location is {loc} for seed {locseed}')
    return loc

# Ideas to speed this up:
# 1) create mapping directly from seed to location
# 2) launch subprocess for each seed_range, calc many at a time (how many threads possible in parallel?)
# 3) after #1, evaluate formulas and only look at lowest value for each (lowest seed value likely)

def solve2(seeds, mapping):
    mapping=complete_mapping(mapping) # fill in 0 to 999,999,999,999,999 (inf)
    locmap=flatten_mapping(mapping)
    loc=None
    part=2
    try:
        for s in seeds:
            try:
                len(s)
            except TypeError:
                s = [s]
                part=1
            for seed in s:
                l = locmap.get(seed)
                if loc is None or l < loc:
                    loc = l
    except Exception as e:
        print(f'Caught exception {e}')
        print(f'seed {seed}')
    print(f'meth2.part{part}:lowest location is {loc}')
    return loc, locmap

def solve3(seeds,rmapping, start_loc=0, incr=1):
    def _in(s,seeds):
        try:
            len(seeds[0])
        except TypeError:
            return s in seeds
        else:
            for sr in seeds:
                if s in sr:
                    return True
            return False
    loc=start_loc
    try:
        while True:
            sd=get_seed(loc,rmapping)
            if _in(sd,seeds):
                print(f"solve3: seed {sd} loc {loc}")
                return sd,loc
            loc=loc+incr
    except KeyboardInterrupt:
        print(f'Caught ctrl+C')
        print(f'solve3 got to location {loc}')
        return get_seed(loc,rmapping), loc

def complete_mapping(mapping):
    for m in mapping.values():
        ranges = sorted(m.maps.keys())
        if ranges[0] != 0:
            m.maps[0]=(ranges[0]-1,0)
        m.maps[m.maps[ranges[-1]][0]+1]=(999999999999999,0)
        # now for rmaps
        rranges = sorted(m.rmaps.keys())
        if rranges[0] != 0:
            m.rmaps[0]=(rranges[0]-1,0)
        m.rmaps[m.rmaps[rranges[-1]][0]+1]=(999999999999999,0)
    return mapping

def flatten_mapping(mapping):
    # now for each intersection in range, flatten
    # create seed-to-fertilizer from seed-to-soil and soil-to-fertilizer
    # and so on...
    fromkey='seed'
    flat = mymap(mm=mapping[fromkey])
    while True:
        tokey=flat.k2
        try:
            m=mapping[tokey]
        except KeyError:
            return flat
        newmaps=join_maps(flat,m)
        flat.maps=newmaps
        flat.k2=m.k2 # the new "tokey"

def join_maps(mm1,mm2): # TODO FIXME this doesn't actually work -- bad algorithm
    m={}
    # find intersections of maps and combine
    allkeys=sorted(list(set(list(mm1.maps.keys())+list(mm2.maps.keys()))))
    print(f"join_maps: \n{pf(mm1.maps)}\n{pf(mm2.maps)}\n{allkeys}")
    k=None
    for k_next in allkeys:
        if k is None:
            k=k_next
            continue
        x=mm1.get(k)
        y=mm2.get(x)
        m[k]=(k_next-1,y-k)
        print(f"join_maps iteration: k {k} k_next {k_next} x {x} y {y} y-k {y-k}")
        k=k_next
    m[k_next]=(999999999999999,0)
    print(f"new map is {m}")
    return m

fn='input.day5'
#fn='sample.day5'
seeds,mapping,rmapping = common(fn)
seeds1,seeds2=seeds
loc1 = solve1(seeds1,mapping)
#loc2 = solve1(seeds2,mapping) # TODO FIXME takes forever with real data
#loc1b, locmap1 = solve2(seeds1,mapping) # TODO FIXME does not work, invalid algorithm
#loc2b, locmap2 = solve2(seeds2,mapping) # TODO FIXME does not work, invalid algorithm
#sd1,l1 = solve3(seeds1,rmapping) # works, but MUCH slower than solve1 method
# TOO LOW: 11815559
# TOO HIGH: 1181555926
# ran solve3 up to loc 18487707
sd2,l2 = solve3(seeds2,rmapping, start_loc=18487707)

ANSWERS='''
meth1.part1:lowest location is 1181555926 for seed 443061598
solve3: seed 1669061417 loc 37806486
'''