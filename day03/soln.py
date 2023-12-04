import re
import numpy as np

with open('input.txt', 'r') as file:
    fline = file.readlines()
# split each line into separate characters
char_matrix = np.array([np.array([char for char in line[:-1]]) for line in fline])
N = len(fline)

## part 1
def check_edge_cases(line_idx, iis):
    """
    checks if the number is in the top row, bottom row, or has
    a character in the first or last column of a given row

    returns bools correspondingly in the order
    first_line, last_line, first_char, last_char
    """
    if line_idx == 0:
        first_line = True
    else:
        first_line = False

    if line_idx == N-1:
        last_line = True
    else:
        last_line = False


    if iis.start() == 0:
        first_char = True
    else:
        first_char = False

    if iis.end() == N:
        last_char = True
    else:
        last_char = False

    return first_line, last_line, first_char, last_char


def check_surrounding_idxs(line_idx, iis):
    """
    """
    symbols = np.array([])
    first_line, last_line, first_char, last_char = check_edge_cases(line_idx, iis)

    if not first_line:
        # can check the line above current line
        if first_char:
            symbols = np.append(symbols, char_matrix[line_idx-1][iis.start():iis.end()+1])
            symbols = np.append(symbols, char_matrix[line_idx][iis.end()])

        elif last_char:
            symbols = np.append(symbols, char_matrix[line_idx-1][iis.start()-1:iis.end()])
            symbols = np.append(symbols, char_matrix[line_idx][iis.start()-1])

        else:
            symbols = np.append(symbols, char_matrix[line_idx-1][iis.start()-1:iis.end()+1])
            symbols = np.append(symbols, char_matrix[line_idx][iis.start()-1])
            symbols = np.append(symbols, char_matrix[line_idx][iis.end()])

    if not last_line:
        # can check the line below current line
        if first_char:
            symbols = np.append(symbols, char_matrix[line_idx+1][iis.start():iis.end()+1])
            symbols = np.append(symbols, char_matrix[line_idx][iis.end()])

        elif last_char:
            symbols = np.append(symbols, char_matrix[line_idx+1][iis.start()-1:iis.end()])
            symbols = np.append(symbols, char_matrix[line_idx][iis.start()-1])

        else:
            symbols = np.append(symbols, char_matrix[line_idx+1][iis.start()-1:iis.end()+1])
            symbols = np.append(symbols, char_matrix[line_idx][iis.start()-1])
            symbols = np.append(symbols, char_matrix[line_idx][iis.end()])

    return symbols

part_nums = []
for line_idx, line in enumerate(fline):
    # find indexes of number in a line
    num_iis = [m for m in re.finditer(r'\d+', line)]

    for iis in num_iis:
        symbols = check_surrounding_idxs(line_idx, iis)
        
        unique_symbols = set(symbols)
        unique_symbols.discard('.')
        if len(unique_symbols) > 0:
            part_nums.append( int(line[iis.start():iis.end()]) )
print(f"part 1: the sum is {sum(part_nums)}")


## part 2
gear_ratios = []
for line_idx, line in enumerate(fline):
    # find indexes of a * character
    char_iis = [m for m in re.finditer(r'\*', line)]

    for iis in char_iis:
        first_line, last_line, first_char, last_char = check_edge_cases(line_idx, iis)
        char_idx = iis.start()
        gear_nums = []

        if not first_line:
            # check line above - is there a number whose indices are adj to the character index?
            num_jjs = [m for m in re.finditer(r'\d+', fline[line_idx-1])]
            for jj in num_jjs:
                if char_idx >= jj.start()-1 and char_idx <= jj.end():
                    gear_nums.append( int(fline[line_idx-1][jj.start():jj.end()]) )

        if not last_line:
            # check line below
            num_jjs = [m for m in re.finditer(r'\d+', fline[line_idx+1])]
            for jj in num_jjs:
                if char_idx >= jj.start()-1 and char_idx <= jj.end():
                    gear_nums.append( int(fline[line_idx+1][jj.start():jj.end()]) )

        # also check the same line, to the left and right
        num_jjs = [m for m in re.finditer(r'\d+', fline[line_idx])]
        for jj in num_jjs:
            if char_idx == jj.start()-1 or char_idx == jj.end():
                gear_nums.append( int(fline[line_idx][jj.start():jj.end()]) )

        # a gear is any * symbol that is adjacent to exactly two part numbers
        if len(gear_nums) == 2:
            gear_ratios.append(gear_nums[0]*gear_nums[1])

print(f"part 2: the sum is {sum(gear_ratios)}")
