import os
from loguru import logger
import sys
logger.remove()
logger.add(sys.stdout, level="INFO")

ROLL = "@"

def is_in_bonds(row, col, cols, rows) -> bool:
    return row >= 0 and row < rows and col >= 0 and col < cols


def get_rolls_in_surroundings(grid: list[list[int]], row, col) -> int:
    sum_roles = 0
    cols = len(grid[0])
    rows = len(grid)
    #left 
    if is_in_bonds(row, col -1, cols, rows) and grid[row][col-1] == ROLL:
        sum_roles += 1
    #right
    if is_in_bonds(row, col + 1, cols, rows) and grid[row][col+1] == ROLL:
        sum_roles += 1    
    #up 
    if is_in_bonds(row+1, col, cols, rows) and grid[row+1][col] == ROLL:
        sum_roles += 1   
    #down
    if is_in_bonds(row-1, col, cols, rows) and grid[row-1][col] == ROLL:
        sum_roles += 1    
    #leftup
    if is_in_bonds(row-1, col-1, cols, rows) and grid[row-1][col-1] == ROLL:
        sum_roles += 1    
    #rightup
    if is_in_bonds(row-1, col+1, cols, rows) and grid[row-1][col+1] == ROLL:
        sum_roles += 1    
    #leftdown
    if is_in_bonds(row+1, col-1, cols, rows) and grid[row+1][col-1] == ROLL:
        sum_roles += 1    
    #rightdown
    if is_in_bonds(row+1, col+1, cols, rows) and grid[row+1][col+1] == ROLL:
        sum_roles += 1
    return sum_roles


def remove_rolls(grid: list[list[int]]):
    """
    return updated plat of rolls + number of taken rolls
    """
    accessible_rolls = 0
    remove_indexes = []
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == ROLL:
                rolls = get_rolls_in_surroundings(grid=grid, row=i, col=j)
                # logger.debug(f"i:{i} | j: {j} | Rolls: {rolls}")
                if rolls < 4:
                    accessible_rolls += 1
                    remove_indexes.append([i, j])
    for item in remove_indexes:
        temp_arr = list(grid[item[0]])
        temp_arr[item[1]] = '.'
        grid[item[0]] = ''.join(temp_arr)
        # grid[item[0]][item[1]] = '.'
    # logger.debug("BEFORE RETURN")
    # print_whole_grid(grid)
    logger.debug(f"Rolls removed: {accessible_rolls}")
    return grid, accessible_rolls


def print_whole_grid(grid: list[list[int]]):
    logger.debug("----------------------")
    for row in grid:
        logger.debug(row)    


def main():
    task_input = None
    file_path = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(file_path, "input.txt"), "r") as f:
        task_input = f.readlines()
    
    task_input = [item.strip() for item in task_input]
    accessible_rolls = 0
    result = 0
    # logger.info(task_input)

    # first half of task    
    # for i in range(len(task_input)):
    #     for j in range(len(task_input[0])):
    #         if task_input[i][j] == ROLL:
    #             rolls = get_rolls_in_surroundings(grid=task_input, row=i, col=j)
    #             logger.debug(f"i:{i} | j: {j} | Rolls: {rolls}")
    #             if rolls < 4:
    #                 accessible_rolls += 1
    
    # Removing rolls with repeating
    new_grid, accessible_rolls = remove_rolls(task_input)
    result += accessible_rolls 
    max_iter = 0
    while accessible_rolls > 0:
        # max_iter += 1
        # if max_iter == 5:
        #     break
        new_grid, accessible_rolls = remove_rolls(new_grid)
        if accessible_rolls == 0:
            break
        print_whole_grid(new_grid)
        result += accessible_rolls
        
    logger.info(f"accessible_rolls: {result}")

if __name__ == "__main__":
    main()