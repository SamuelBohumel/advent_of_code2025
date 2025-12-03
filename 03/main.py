import os
from loguru import logger
import sys
from itertools import combinations
from combinations import Combination

logger.remove()
logger.add(sys.stdout, level="DEBUG")

def rSubset(arr, r):
    return list(combinations(arr, r))

def get_number_from_digits(numbers):
    # result = 0
    # length = len(numbers)
    # for i in range(length, -1, -1):
    #     result += numbers[i] * (10** (length-i))
    # return result
    strings = [str(num) for num in numbers]
    return int(''.join(strings))

# def get_highest_joltage(baterries: str) -> int:
#     voltages = [int(num.strip()) for num in baterries.strip()]
#     logger.debug(voltages)
#     r = 2
#     com = Combination(voltages, r)
#     maximum = 0
#     com.GetFirst()
#     while (com.HasNext()) :
#         combination = com.Next()
        
#         logger.debug(combination)
#         number = get_number_from_digits(combination)
#         if number > maximum:
#             maximum = number
        

#     logger.info(f"Maximum: {maximum}")
#     return maximum


def get_highest_joltage(batteries: str) -> int:
    voltages = [int(num.strip()) for num in batteries.strip()]
    r = 12  # size of combination
    n = len(voltages)

    # Initialize indices for first combination
    indices = list(range(r))
    maximum = 0

    while True:
        # Build current combination
        combination = [voltages[i] for i in indices]
        number = get_number_from_digits(combination)
        if number > maximum:
            maximum = number

        # Generate next combination
        # Find the rightmost index that can be incremented
        for i in reversed(range(r)):
            if indices[i] != i + n - r:
                break
        else:
            # All combinations generated
            break

        indices[i] += 1
        for j in range(i + 1, r):
            indices[j] = indices[j - 1] + 1

    logger.info(f"Maximum: {maximum}")
    return maximum


    

def main():
    task_input = None
    file_path = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(file_path, "input.txt"), "r") as f:
        task_input = f.readlines()
    
    # logger.info(task_input)
    outputs = []
    for battery_rack in task_input:
        outputs.append(get_highest_joltage(battery_rack))

    logger.info(f"Sum: {sum(outputs)}")

if __name__ == "__main__":
    main()