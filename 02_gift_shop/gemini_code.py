# Assuming the input is loaded into a variable named task_input (a list of lines)
# task_input = ["11-22,95-115,998-1012,1188511880-1188511890,222220-222224,1698522-1698528,446443-446449,38593856-38593862,565653-565659,824824821-824824827,2121212118-2121212124,9007199254740990-9007199254740991"]

import os

# Define the file path and read the input
file_path = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(file_path, "input.txt"), "r") as f:
    task_input = f.readlines()
    
# Clean up and parse the ranges
ranges_str = "".join(line.strip() for line in task_input)
ranges_list = []
for r in ranges_str.split(','):
    start, end = map(int, r.split('-'))
    ranges_list.append((start, end))
    
total_sum = 0
# The maximum ID is 9007199254740991, which has 16 digits.
# Max k (half-length) is 16 // 2 = 8.
MAX_K = 8

for k in range(1, MAX_K + 1):
    # k is the length of the repeating sequence S
    
    # Calculate the multiplier M = 10^k + 1
    multiplier = 10**k + 1
    
    # Determine the range of S (S must not have a leading zero)
    # Smallest S is 1 followed by k-1 zeros (10^(k-1))
    start_S = 10**(k - 1)
    # Largest S is k nines (10^k - 1)
    end_S = 10**k - 1
    
    for S in range(start_S, end_S + 1):
        # Calculate the invalid ID N = S * M
        N = S * multiplier
        
        # Check if N is within any of the given ranges
        for start, end in ranges_list:
            if start <= N <= end:
                total_sum += N
                # Once an invalid ID is found and summed, we can stop checking
                # it against other ranges, as the problem asks for the sum of 
                # all *unique* invalid IDs present in *any* range.
                break 

print(f"The sum of all invalid IDs is: {total_sum}")