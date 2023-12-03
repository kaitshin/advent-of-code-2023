import re
import numpy as np

with open('input.txt', 'r') as file:
    fline = file.readlines()

nums_only = np.array([re.sub("[^0-9]", "", line) for line in fline])
soln_str = np.array([num+num if len(num)==1 else num[0]+num[-1] for num in nums_only])
print(f"the sum is {soln_str.astype(int).sum()}")
