import os
from loguru import logger
import sys
import copy
import itertools
logger.remove()
logger.add(sys.stdout, level="INFO")

START = "S"
SPLITTER = "^"
BEAM = "|"
EMPTY_SPACE = "."

def print_tachyon_manifold(tachyon_map: list[str]):
    for row in tachyon_map:
        logger.debug(''.join(row))
    logger.debug('X'*len(tachyon_map))

def count_beams(tachyon_map: list[str]) -> int:
    beam_count = 0
    for row in tachyon_map:
        for char in row:
            if char == BEAM:
                beam_count += 1
    return beam_count

def tachyon_flow_task_1(tachyon_map: list[str]) -> int:
    split_count = 0
    # find first S
    for i in range(len(tachyon_map[0])):
        if tachyon_map[0][i] == START:
            start_index = i
    #apply first step: beam from start
    tachyon_map[1][start_index] = BEAM
    # now iterate next rows
    for i in range(2, len(tachyon_map)):
        for j in range(len(tachyon_map[i])):
            # if there is beam above us, just continue the beam
            if tachyon_map[i-1][j] == BEAM and tachyon_map[i][j] == EMPTY_SPACE:
                logger.debug(f"i: {i} | j: {j} | char: {tachyon_map[i][j]} | i-1 char: {tachyon_map[i-1][j]}")
                tachyon_map[i][j] = BEAM
            if tachyon_map[i-1][j] == BEAM and tachyon_map[i][j] == SPLITTER:
                split_count += 1
                logger.debug(f"i: {i} | j: {j} | char: {tachyon_map[i][j]} | i-1 char: {tachyon_map[i-1][j]}")
                #put beams left and right, but check indexes first
                if j > 0:
                    tachyon_map[i][j-1] = BEAM
                if j < len(tachyon_map[i]) - 1:
                    tachyon_map[i][j+1] = BEAM
        # print_tachyon_manifold(tachyon_map=tachyon_map)   
    return split_count


def get_timelines(position: str, paths: list[str]):
    # logger.debug(f"position: {position} | paths: {paths}")
    numbers = paths[0]
    count_left, count_right, count_middle = 0, 0, 0
    for number in numbers:
        if position - 1 == number:
            if len(paths) == 1:
                return 1
            count_left += get_timelines(position=number, paths=paths[1:])
        if position + 1 == number:
            if len(paths) == 1:
                return 1
            count_right += get_timelines(position=number, paths=paths[1:])
        if number == position:
            if len(paths) == 1:
                return 0
            count_middle += get_timelines(position=number, paths=paths[1:])

    logger.debug(f"left: {count_left} |  right: {count_right}")
    return count_left + count_right + count_middle


#Alterantive timelines
def get_map(tachyon_map: list[str]) -> int:
    #setup a list of branches
    paths = []
    # find first S
    for i in range(len(tachyon_map[0])):
        if tachyon_map[0][i] == START:
            start_index = i
    #apply first step: beam from start
    tachyon_map[1][start_index] = BEAM
    paths.append([start_index])
    # now iterate next rows
    for i in range(2, len(tachyon_map)):
        arr = []
        for j in range(len(tachyon_map[i])):
            # if there is beam above us, just continue the beam
            if tachyon_map[i-1][j] == BEAM and tachyon_map[i][j] == EMPTY_SPACE:
                tachyon_map[i][j] = BEAM
            if tachyon_map[i-1][j] == BEAM and tachyon_map[i][j] == SPLITTER:
                #put beams left and right, but check indexes first
                if j > 0:
                    tachyon_map[i][j-1] = BEAM

                if j < len(tachyon_map[i]) - 1:
                    tachyon_map[i][j+1] = BEAM
    #count beams to see routes
    for i in range(2, len(tachyon_map)):
        arr = []
        for j in range(len(tachyon_map[i])):
            if tachyon_map[i][j] == BEAM:
              arr.append(j)  
        paths.append(arr)
    print_tachyon_manifold(tachyon_map=tachyon_map)  
    for path in paths:
        logger.debug(path) 
    # timeline_count = get_timelines(position=paths[0][0], paths=paths[1:4])
    return paths


def path_possible(path: list[str], original_map) -> bool:
    """
    iterate backwards and check if diffference is 0 or 1
    """
    if len(path) <=5:
        range_control = range(0, len(path)-1)
    else:
        range_control = range(len(path)-3,len(path)-1)
    for i in range(0, len(path)-1):
        possible_range = list(range(path[i]-1, path[i]+2 ))
        if path[i+1] not in possible_range:
            return False
        #check if ther is a splitter
        logger.debug(f"path[i+1]: {path[i+1]} | path[i]: {path[i]} | left: {original_map[i+1][path[i]]} | right {original_map[i+1][path[i]]}")
        if path[i+1] < path[i] and original_map[i+1][path[i]] != SPLITTER:    #left split
            return False
        if path[i+1] > path[i] and original_map[i+1][path[i]] != SPLITTER:    #right split
            return False

    return True

def get_timelines_iterative(tachyon_map: list[str], original_map: list[str]) -> int:
    timelines = 0
    orig_map_length = len(original_map)
    existing_paths = [[tachyon_map[0][0]]]
    for i in range(1, len(tachyon_map)):
        logger.info(f"Processing row: {i}/{len(tachyon_map)}")
        new_paths = []
        for j in range(len(tachyon_map[i])):
            for z in range(len(existing_paths)):
                maybe_new = existing_paths[z] + [(tachyon_map[i][j])]
                # logger.info(f"{maybe_new} | {len(original_map)}")
                if path_possible(maybe_new, original_map[1:]):
                    new_paths.append(maybe_new)
        del existing_paths 
        existing_paths = new_paths
        logger.info(f"New paths length: {len(new_paths)}")
    #drop duplicate lists
    existing_paths.sort()
    unique_paths = list(lis for lis,_ in itertools.groupby(existing_paths))
    timelines = len(unique_paths)
    return timelines

def main():
    task_input = None
    file_path = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(file_path, "input.txt"), "r") as f:
        task_input = f.readlines()
    
    task_input = [list(line.strip()) for line in task_input]
    logger.info(task_input)

    count = tachyon_flow_task_1(tachyon_map=copy.deepcopy(task_input))

    logger.info(f"Main manifold:")
    print_tachyon_manifold(task_input)
    filled_map = get_map(tachyon_map=copy.deepcopy(task_input))
    # timelines = tachyon_flow_task_2(tachyon_map=copy.deepcopy(task_input))
    timelines = get_timelines_iterative(tachyon_map=copy.deepcopy(filled_map), 
                                        original_map=copy.deepcopy(task_input))
    logger.info(f"Total beams: {count}")
    logger.info(f"Timelines: {timelines}")


if __name__ == "__main__":
    main()