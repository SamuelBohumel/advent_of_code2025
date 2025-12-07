import os
from loguru import logger
import sys
import copy
logger.remove()
logger.add(sys.stdout, level="DEBUG")

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
    if paths == []:
        return 0
    numbers = paths[0]
    left, right, middle = None, None, None
    count_left, count_right = 0, 0
    for number in numbers:
        if position - 1 == number:
            left = number
        if position + 1 == number:
            right = number
        if number == position:
            middle = number
    if left is not None:
        count_left = get_timelines(position=left, paths=paths[1:])
    if right is not None:
        count_right = get_timelines(position=right, paths=paths[1:])
    if middle is not None:
        get_timelines(position=middle, paths=paths[1:])

    logger.debug(f"left: {count_left} |  right: {count_right}")
    return 1 + count_left + count_right


#Alterantive timelines
def tachyon_flow_task_2(tachyon_map: list[str]) -> int:
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
    timeline_count = get_timelines(position=paths[0][0], paths=paths[1:4])
    return timeline_count


def main():
    task_input = None
    file_path = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(file_path, "ex_input.txt"), "r") as f:
        task_input = f.readlines()
    
    task_input = [list(line.strip()) for line in task_input]
    logger.info(task_input)

    count = tachyon_flow_task_1(tachyon_map=copy.deepcopy(task_input))

    logger.info(f"Main manifold:")
    print_tachyon_manifold(task_input)
    timelines = tachyon_flow_task_2(tachyon_map=copy.deepcopy(task_input))
    logger.info(f"Total beams: {count}")
    logger.info(f"Timelines: {timelines}")


if __name__ == "__main__":
    main()