import os
from loguru import logger
import sys
from itertools import combinations


logger.remove()
logger.add(sys.stdout, level="INFO")

def get_max_number_index(array: list[int]) -> int:
    #return highest number with lowest index
    max_number = -1
    max_index = -1
    for i, current in reversed(list(enumerate(array))):
        if current >= max_number:
            max_number = current
            max_index = i
    return max_index
    

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

def get_highest_joltage(batteries: str) -> int:
    voltages = [int(num.strip()) for num in batteries.strip()]
    logger.debug(f"Voltages: {voltages}")
    r = 12  # size of combination
    n = len(voltages)
    lower_index = 0
    final_nums = []
    for i in range(r):
        logger.debug(f"i: {i} | boundary: {lower_index}:{n - r + i + 1} | length: {n}")
        array = voltages[lower_index:n - r + i + 1]
        max_index = get_max_number_index(array)
        logger.debug(f"Max index: {max_index} | Max number: {voltages[max_index]}")
        final_nums.append(voltages[lower_index + max_index])
        lower_index += max_index + 1

    # join numbers
    maximum = int("".join([str(num) for num in final_nums]))
    return maximum

def get_highest_joltage_old(baterries: str) -> int:
    voltages = [int(num.strip()) for num in baterries.strip()]
    # logger.debug(voltages)
    r = 12
    maximum = 0
    combinations = rSubset(voltages, r)
    # logger.info(len(combinations))
    for comb in combinations:
        number = get_number_from_digits(comb)
        if number > maximum:
            maximum = number
    return maximum

    

def main():
    task_input = None
    file_path = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(file_path, "input.txt"), "r") as f:
        task_input = f.readlines()
    
    # logger.info(task_input)
    outputs = []
    for battery_rack in task_input:
        number1 = get_highest_joltage(battery_rack)
        # number2 = get_highest_joltage_old(battery_rack)
        # if number1 != number2:
        #     logger.error(f"Mismatch! {number1} != {number2}")
        #     logger.info(f"Battery rack: {battery_rack}")
        logger.info(f"Highest joltage for rack {battery_rack.strip()}: {number1}")
        outputs.append(number1)

    logger.info(f"Sum: {sum(outputs)}")

if __name__ == "__main__":
    main()