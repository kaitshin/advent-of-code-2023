import numpy as np
import copy

with open('input.txt', 'r') as file:
    fline_orig = file.read().splitlines()

## part 1
def get_seeds(line):
    """
    assumes first line looks like
    `seeds: 79 14 55 13`
    and returns a list of just the numbers
    """
    seeds = line.split(' ')[1:]
    return np.array([int(num) for num in seeds])

def get_rule_iis(fline):
    """
    gets the indexes of the fline array (after the seeds input) that set
    what the rules are for each map

    does so by looking at the indexes of the fline array that are in between
    lines that contain 'map' and empty newlines, since the input.txt is
    formatted as
    map:
    rule
    rule
    [newline]
    map:
    rule
    rule
    rule
    [etc]

    rule_iis is then returned as a list of tuples; for the mini-example above,
    the return value would be [(1,2), (5,6,7)]
    """
    fline = np.append(fline, '')
    tmp_maplists = [x for x in range(len(fline)) if 'map' in fline[x] or len(fline[x])==0]
    rule_iis = [np.arange(tmp_maplists[i]+1, tmp_maplists[i+1])
        for i in np.arange(len(tmp_maplists)-1, step=2)]

    return rule_iis

seeds = get_seeds(fline_orig[0])
fline = np.array(fline_orig[2:]) # starts after the seeds line
rule_iis = get_rule_iis(fline)

# now iterates over a set of rules (e.g., by seed-to-soil and then soil-to-fertilizer)
for iis in rule_iis:
    # takes the indexes where the rules are in input file and turns them into np.ndarrays
    list_of_rule_lists = np.array([ np.array([int(y) for y in x.split(' ')]) for x in fline[iis] ])
    
    # gets ranges and shifting vals according to the list of rule lists
    ranges = [(rule_list[1],rule_list[1]+rule_list[2]) for rule_list in list_of_rule_lists]
    shifts = np.array([rule_list[1]-rule_list[0] for rule_list in list_of_rule_lists])

    # for each seed, shifts the values accordingly
    for ii, seed in enumerate(seeds):
        for jj in range(len(ranges)):
            if (seed>=ranges[jj][0] and seed<ranges[jj][1]):
                seeds[ii] = seed-shifts[jj]
print(f"part 1: the lowest location number is {np.min(seeds)}")


## part 2
# instead of working with seeds, now working with ranges of seeds
def get_seed_ranges(line):
    """
    assumes first line looks like
    `seeds: 79 14 55 13`
    and returns a list of [[79,...,79+14], [55,...,55+13]] just the numbers
    """
    seeds = [int(num) for num in line.split(' ')[1:]]
    seed_ranges = [np.array([seeds[i], seeds[i]+seeds[i+1]]) for i in np.arange(len(seeds), step=2)]

    return seed_ranges

def split_array(input_arr, range_list):
    """
    takes an input_arr (the "seeds")
    takes also a list of ranges (the "rule ranges")
    splits up the input arr depending on the input list of ranges and returns the corresponding index

    e.g., let's say the list of ranges is
        [[11, 53],[53, 61],[67,89]]

    (1) there's no overlap at all: input_arr = [2,10]
        returns [[2,10]], idx=[-1] (for no overlap at all)
    (1.5): input_arr = [100,105]
        returns [[100,105]], idx=[-1]
    (1.75): input_arr = [62,65]
        returns [[62,65]], idx=[-1]

    (2) there's complete overlap within one case: input_arr = [55,60]
        returns [[55,60]], idx=[1] (for complete overlap with first range)

    (3) there's partial overlap: input_arr = [55,80]
        returns [[55,61],[61,67],[67,80]], idx=[1,-1,2]

    (4) there's partial overlap with the edges: input_arr = [2, 100]
        returns [[2,11],[11,53],[53, 61],[61,67],[67,89],[89,100]], idx = [-1,0,1,-1,2,-1]
    """
    frange_list = range_list.flatten()
    min_num = input_arr[0]
    max_num = input_arr[1]

    # case (1)
    if max(input_arr) < min(frange_list):
        return np.array([input_arr]), np.array([-1])

    # case (1.5)
    if min(input_arr) >= max(frange_list):
        return np.array([input_arr]), np.array([-1])

    # the fun cases
    min_idx = np.where(min_num >= frange_list)[0]
    if len(min_idx) == 0:
        min_idx = -1
    else:
        min_idx = min_idx[-1]

    max_idx = np.where(max_num < frange_list)[0]
    if len(max_idx) == 0:
        max_idx = len(frange_list)
    else:
        max_idx = max_idx[0]

    idx_range = np.arange(min_idx//2, max_idx//2+1)
    if len(idx_range) == 1:
        return np.array([input_arr]), idx_range

    # case (1.75)
    elif len(idx_range)==2 and (idx_range[1]-idx_range[0])==1 and idx_range[1]%2==0:
        return np.array([input_arr]),  np.array([-1])

    else:
        output_arr = []
        output_idx = []
        for ctr, ii in enumerate(idx_range):
            # overlapping with lowest range
            if ii == -1:
                output_arr.append([min_num, frange_list[0]])
                output_idx.append(-1)
            # overlapping with highest range
            elif ii == len(range_list):
                output_arr.append([frange_list[-1], max_num])
                output_idx.append(-1)

            else:
                range_min = range_list[ii][0]
                range_max = range_list[ii][1]

                # check for a 'hole'
                if (ctr > 0) and (range_min-range_list[ii-1][1] > 0):
                    output_arr.append([ range_list[ii-1][1], range_min ])
                    output_idx.append(-1)

                output_arr.append([np.max([min_num, range_min]), np.min([max_num, range_max])])
                output_idx.append(ii)

                # check for last 'hole'
                if (ctr == len(idx_range)-1) and (max_num > range_max):
                    output_arr.append([ range_max, max_num ])
                    output_idx.append(-1)

        return np.array(output_arr), np.array(output_idx)

def clean_to_list_of_arrs(mapped_seed_ranges):
    """
    cleans input `mapped_seed_ranges` to flatten all subarrays
    e.g., we go from
        [array([1,2]), array([[3,4],[5,6]])]
    to
        [array([1,2]), array([3,4]), array([5,6])]
    """
    cleaned_msranges = []
    for arr in mapped_seed_ranges:
        if arr.shape==(2,):
            cleaned_msranges.append(arr)
        else:
            for subarr in arr:
                cleaned_msranges.append(subarr)
    return cleaned_msranges


seed_ranges = get_seed_ranges(fline_orig[0])
# iterates over same set of rules obtained in part 1
for iis in rule_iis:
    # takes the indexes where the rules are in input file and turns them into np.ndarrays
    list_of_rule_lists = np.array([ np.array([int(y) for y in x.split(' ')]) for x in fline[iis] ])
    
    # gets ranges and shifting vals according to the list of rule lists
    ranges = np.array([np.array([rule_list[1],rule_list[1]+rule_list[2]]) for rule_list in list_of_rule_lists])
    shifts = np.array([rule_list[1]-rule_list[0] for rule_list in list_of_rule_lists])

    # sorts the ranges in numerical order and sorts the shifts accordingly
    sort_iis = np.argsort(ranges, axis=0)[:,0]
    ranges = ranges[sort_iis]
    shifts = shifts[sort_iis]

    # goes over each set of seed_ranges, splits them according to the rule ranges,
    # and based on how they're split, applies the corresponding shift (or lack thereof)
    mapped_seed_ranges = []
    for ss, seed_range in enumerate(seed_ranges):
        split_seeds, rule_jjs = split_array(seed_range, ranges)

        for j_idx, jj in enumerate(rule_jjs):
            if jj < 0:
                mapped_seed_ranges.append(split_seeds[j_idx])
            else:
                mapped_seed_ranges.append(split_seeds[j_idx] - shifts[jj])

    # cleans up the mapped seed ranges to get a list of arrays
    seed_ranges = clean_to_list_of_arrs(mapped_seed_ranges)
print(f"part 2: the lowest location number is {np.min(seed_ranges)}")
