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


def get_timelines_iterative(tachyon_map: list[str], original_map: list[str]) -> int:
    # Start at the X-position found in the first row of tachyon_map
    start_x = tachyon_map[0].index(tachyon_map[0][0])
    
    # Dictionary mapping x → number of timelines at that position
    x_to_t_count = {start_x: 1}

    # Iterate through each subsequent row
    for i in range(1, len(tachyon_map)):
        row = original_map[i]
        new_counts: dict[int, int] = {}

        for x, count in x_to_t_count.items():
            cell = row[x]

            if cell == SPLITTER:
                # Branch to left and right
                for nx in (x - 1, x + 1):
                    if 0 <= nx < len(row):   # bounds check
                        if nx in tachyon_map[i]:  # must be a valid tachyon position
                            new_counts[nx] = new_counts.get(nx, 0) + count
            else:  # EMPTY_SPACE or anything else
                if x in tachyon_map[i]:
                    new_counts[x] = new_counts.get(x, 0) + count

        x_to_t_count = new_counts

    # Total number of possible timelines that reach the last row
    return sum(x_to_t_count.values())

def input_lines(original_map):
    for line in original_map:
        yield line

def get_timelines_iterative_2(original_map: list[str]):


    total = 0
    rows = input_lines(original_map)

    x_to_t_map = {next(rows).index(START): 1}
    for row in rows:
        new_x_to_t_map: dict[int, int] = {}
        for x, t in x_to_t_map.items():
            for x in (x,) if row[x] != SPLITTER else (x - 1, x + 1):
                new_x_to_t_map[x] = new_x_to_t_map.get(x, 0) + t
        x_to_t_map = new_x_to_t_map

    total = sum(x_to_t_map.values())

    return total


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
                                        original_map=copy.deepcopy(task_input[1:]))
    timelines = get_timelines_iterative_2(original_map=task_input)
    logger.info(f"Total beams: {count}")
    logger.info(f"Timelines: {timelines}")


if __name__ == "__main__":
    main()