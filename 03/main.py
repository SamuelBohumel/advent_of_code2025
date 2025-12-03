import os
from loguru import logger
import sys
from itertools import combinations

logger.remove()
logger.add(sys.stdout, level="INFO")

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

def get_highest_joltage(baterries: str) -> int:
    voltages = [int(num.strip()) for num in baterries.strip()]
    logger.debug(voltages)
    r = 12
    maximum = 0
    combinations = rSubset(voltages, r)
    logger.info(len(combinations))
    for comb in combinations:
        number = get_number_from_digits(comb)
        if number > maximum:
            maximum = number
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