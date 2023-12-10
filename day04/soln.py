with open('input.txt', 'r') as file:
    fline = file.readlines()

def clean_str_array_of_nums_spaces(arr):
    """
    assumes an input list/array of strings that contain
    either integers or spaces

    returns a list of only the integers, as dtype int
    """
    return [int(num) for num in arr if len(num)>0]

## part 1
card_points = []
for line in fline:
    winning_nums = line.split('|')[0].split(':')[1].split(' ')
    winning_nums = clean_str_array_of_nums_spaces(winning_nums)

    drawn_nums = line.split('|')[1].split(' ')
    drawn_nums = clean_str_array_of_nums_spaces(drawn_nums)

    n=0
    for num in drawn_nums:
        if num in winning_nums:
            n+=1
    
    if n>0:
        card_points.append(2**(n-1))
print(f"part 1: the sum is {sum(card_points)}")


## part 2
# populate with original cards
card_count = {}
for i in range(len(fline)):
    card_count[i+1]=1

# go through and see for each game, what games you win a copy of
for ii, line in enumerate(fline):
    winning_nums = line.split('|')[0].split(':')[1].split(' ')
    winning_nums = clean_str_array_of_nums_spaces(winning_nums)

    drawn_nums = line.split('|')[1].split(' ')
    drawn_nums = clean_str_array_of_nums_spaces(drawn_nums)

    origcard_num = ii+1
    copycard_num = 0
    round_count = {}
    for num in drawn_nums:
        if num in winning_nums:
            copycard_num+=1
            # adds copies of card won from original card
            round_count[origcard_num+copycard_num] = card_count[origcard_num+copycard_num] + card_count[origcard_num]

    # updating the total number of cards with the per-round copies added
    for key in round_count:
        card_count[key] = round_count[key]

print(f"part 2: the sum is {sum(card_count.values())}")
