import numpy as np

with open('input.txt', 'r') as file:
    fline = file.read().splitlines()

## part 1
def travel_dist(race_dur, thold):
    """
    race_dur = duration of the race
    thold = time you hold the button
        ranges from 0 to race_dur ms
    """
    return thold * (race_dur-thold)

race_durs = [int(num) for num in fline[0].split(' ')[1:] if len(num)>0]
records = [int(num) for num in fline[1].split(' ')[1:] if len(num)>0]

newrecs = []
for race_dur, record in zip(race_durs, records):
    ctr = 0
    for th in np.arange(race_dur+1):
        if travel_dist(race_dur, th) > record:
            ctr += 1
    newrecs.append(ctr)
print(f"part 1: the margin of error is {np.prod(newrecs)}")


## part 2
big_race_dur = int(''.join( fline[0].split(' ')[1:] ))
big_record = int(''.join( fline[1].split(' ')[1:] ))
ctr = 0
for th in np.arange(big_race_dur+1):
    if travel_dist(big_race_dur, th) > big_record:
        ctr += 1
print(f"part 2: the margin of error is {ctr}")
