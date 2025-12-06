import os
from loguru import logger
import sys
logger.remove()
logger.add(sys.stdout, level="DEBUG")

class Number():

    def __init__(self, number: int, row: int, col: int, problem_id: int) -> None:
        self.number = number
        self.row = row
        self.col = col
        self.problem_id = problem_id

    def __str__(self):
        return f"number: {self.number} | row: {self.row} | col: {self.col} | problem_id: {self.problem_id}"   
    

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

def swap_numbers(numbers: list[str]) -> list[str]:
    """
    Each number is given in its own column, with the most 
    significant digit at the top and the least significant 
    digit at the bottom.
    from numbers:
    64
    23
    314
    create: 623, 431 and 4
    """
    max_length_num = max([len(number) for number in numbers])
    new_list = ["" for i in range(max_length_num)]
    logger.debug(numbers)
    for number in numbers:
        for j in range(len(number)):
            index = max_length_num - len(number) + j
            new_list[index] += str(number[j])
    return new_list


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

def count_problems_task2(problems: list[list], rows: int, cols: int) -> int:
    grand_total = 0
    for problem in problems:
        problem = problem.replace("\n", "")
        logger.debug(problem)
    all_numbers = []
    for i, row in enumerate(problems[:-1]):
        problem_id = 0
        for j, character in enumerate(row):
            if character != " ":
                all_numbers.append(Number(
                    number=character,
                    row=i,
                    col=j,
                    problem_id=problem_id
                ))
            if j > 0 and character == " " and row[j-1].isnumeric():
                problem_id += 1
    numbers = {}
    for num in all_numbers:
        logger.debug(num)
        if num.problem_id not in numbers.keys():
            numbers[num.problem_id] = {}
        if num.col not in numbers[num.problem_id].keys():
            numbers[num.problem_id] = {}
        numbers[num.problem_id][num.col] += num.number
    logger.debug(numbers)



def main():
    task_input = None
    file_path = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(file_path, "ex_input.txt"), "r") as f:
        orig_task_input = f.readlines()
    
    #clear input and split by space
    task_input = [string.strip().split(" ") for string in orig_task_input]
    logger.debug(f"task_input: {task_input}") 
    #remove empty elements
    problems = []
    for row in task_input:
        arr = []
        for item in row:
            if item != '':
                arr.append(item)
        problems.append(arr)
    rows, numbers_in_row = len(problems), len(problems[0])
    # logger.debug(f"cleared_input: {problems}") 
        
    # total = count_problems(problems)
    # logger.info(f"Total (task 1): {total}")
    total2 = count_problems_task2(problems=orig_task_input, rows=rows, cols=numbers_in_row)
    logger.info(f"Total (task 2): {total2}")


if __name__ == "__main__":
    main()