import os
from loguru import logger
import sys
logger.remove()
logger.add(sys.stdout, level="INFO")

def compute_problem(problem: list[str]) -> list[str]:
    """
    Takes string array with 3 elements: operator and two numbers, 
    return operator and result of that operation in array
    """
    operator = problem[0]
    num1 = problem[1]
    num2 = problem[2]
    if operator == '+':
        result = int(num1) + int(num2)
    elif operator == '*':
        result = int(num1) * int(num2)
    else:
        raise Exception(f"Unknown operator: {operator}")
    return [operator, str(result)]


def count_problems(problems: list[list]) -> int:
    grand_total = 0
    cleared_problems = []
    for i in range(len(problems[0])):
        cleared_problems.append([]) 
    logger.info(f"Initialized cleared_problems: {len(cleared_problems)}")
    for item in reversed(problems):
        for j, operator in enumerate(item):
            cleared_problems[j].append(operator)
            #compute if there is operaotor and new two numbers
            if len(cleared_problems[j]) == 3:
                # logger.debug(cleared_problems)
                cleared_problems[j] = compute_problem(cleared_problems[j])
    logger.debug(cleared_problems)

    #count second elements of each problem
    for solved_problem in cleared_problems:
        grand_total += int(solved_problem[1])

    return grand_total


def main():
    task_input = None
    file_path = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(file_path, "input.txt"), "r") as f:
        task_input = f.readlines()
    
    #clear input and split by space
    task_input = [string.strip().split(" ") for string in task_input]
    logger.debug(f"task_input: {task_input}") 
    #remove empty elements
    problems = []
    for row in task_input:
        arr = []
        for item in row:
            if item != '':
                arr.append(item)
        problems.append(arr)
    logger.debug(f"cleared_input: {problems}") 
    # check lengths
    for row in problems:
        logger.info(f"length: {len(row)}")
        
    total = count_problems(problems)
    logger.info(f"Total: {total}")


if __name__ == "__main__":
    main()