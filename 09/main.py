import os
from loguru import logger
import sys
import math
logger.remove()
logger.add(sys.stdout, level="INFO")

def get_largest_rectangle(coords: list[list[int]]) -> int:
    length = len(coords)
    areas = []
    max_area = 0
    for i in range(length):
        row = []
        for j in range(length):
            if j < i:
                #compute area
                a = abs(coords[i][0] - coords[j][0])+1  # +1 because its inclusive
                b = abs(coords[i][1] - coords[j][1])+1
                area = a * b
                logger.debug(f"x:{coords[i][0]} y:{coords[i][1]}| x:{coords[j][0]} y:{coords[j][1]}| a:{a} | b {b} | area:{area}")
                if area > max_area:
                    max_area = area
                row.append(area)
        areas.append(row)
    for row in areas:
        logger.debug(row)
    return max_area


def main():
    task_input = None
    file_path = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(file_path, "input.txt"), "r") as f:
        task_input = f.readlines()
    
    task_input = [line.strip() for line in task_input]
    numbers = []
    for line in task_input:
        numbers.append([int(num) for num in line.split(",")])
    logger.info(numbers)

    max_area = get_largest_rectangle(coords=numbers)
    logger.info(f"Task 1 result: {max_area}")


if __name__ == "__main__":
    main()