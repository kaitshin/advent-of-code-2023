import re
import numpy as np

with open('input.txt', 'r') as file:
    fline = file.readlines()

# part 1
nums_only = np.array([re.sub("[^0-9]", "", line) for line in fline])
soln_str = np.array([num[0]+num[-1] for num in nums_only])
print(f"part 1: the sum is {soln_str.astype(int).sum()}")

## part 2
txt2num = {
    'one': '1',
    'two': '2',
    'three': '3',
    'four': '4',
    'five': '5',
    'six': '6',
    'seven': '7',
    'eight': '8',
    'nine': '9'
}
def text_to_int(line):
    match_iis = np.array([])
    match_dict = np.array([])
    for txt in txt2num:
        idx_matches = [m.start() for m in re.finditer(txt, line)]
        if len(idx_matches) > 0:
            match_iis = np.append(match_iis, idx_matches)
            match_dict = np.append(match_dict, [txt]*len(idx_matches))

    sorted_matches = np.array(match_dict)[np.argsort(match_iis)]
    for txt in sorted_matches:
        line = re.sub(fr'({txt[:1]})+({txt[1:]})', rf'\g<1>{txt2num[txt]}\g<2>', line, 1)

    return line

text_to_int = np.array([text_to_int(line) for line in fline])
nums_only = np.array([re.sub("[^0-9]", "", line) for line in text_to_int])
soln_str = np.array([num[0]+num[-1] for num in nums_only])
print(f"part 2: the sum is {soln_str.astype(int).sum()}")
