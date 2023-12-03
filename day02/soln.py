import re
import numpy as np

with open('input.txt', 'r') as file:
    fline = file.readlines()

# part 1
def check_num_for_color_possible(line, color):
    """
    helper fn for `is_game_possible`
    """
    game_dict = {'red': 12, 'green': 13, 'blue': 14}
    all_color = re.findall(rf'\d+ {color}', line)
    shown_cubes = np.array([int(result.split(' ')[0]) for result in all_color])
    if len(np.where(shown_cubes > game_dict[color])[0]) == 0:
        return True
    else:
        return False

def is_game_possible(line):
    """
    if it's possible, return the game id number
    otherwise return 0
    """
    possible_arr = []
    for color in ['red', 'green', 'blue']:
        possible_arr.append(check_num_for_color_possible(line, color))

    if False in possible_arr:
        return 0
    else:
        game_id = int(re.findall(r'\d+', line)[0])
        return game_id

result = []
for line in fline:
    result.append(is_game_possible(line))
print(f"part 1: the sum is {sum(result)}")