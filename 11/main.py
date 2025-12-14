import os
from loguru import logger
import sys
from functools import cache
logger.remove()
logger.add(sys.stdout, level="INFO")



def create_graph(lines) -> dict:
    graph = {}
    for line in lines:
        splitted = line.split(" ")
        key = splitted[0].replace(":", "")
        values = splitted[1:]
        graph[key] = values
    return graph


def find_outs(current_key: str, graph: dict) -> int:
    count = 0
    if current_key == 'out':
        return 1
    for key in graph[current_key]:
        count += find_outs(key, graph)
        
    return count



def find_outs_with_fft_tty(graph: dict) -> int:
    
    @cache
    def find_paths(current_key: str, visited_dac:bool, visited_fft: bool): 
        count = 0
        if current_key == 'out':
            if visited_dac and visited_fft:
                return 1
            else:
                return 0
        keys = graph.get(current_key)
        if keys is None:
            return 0
        for key in keys:
            if key == "dac":
                visited_dac = True
            elif key == "fft":
                visited_fft = True            
            count += find_paths(key, visited_dac=visited_dac, visited_fft=visited_fft)
            
        return count
    
    return find_paths("svr", False, False)


def main():
    
    task_input = None
    file_path = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(file_path, "input.txt"), "r") as f:
        task_input = f.readlines()
        task_input = [line.strip() for line in task_input]
        

    graph = create_graph(task_input)

    logger.info(f"keys: {len(graph.keys())}")
    #task 1
    out_paths = find_outs("you", graph)
    logger.info(f"Out paths: {out_paths}")
    #task 2
    out_paths_visited_ppy = find_outs_with_fft_tty(graph)
    logger.info(f"out_paths_visited_ppy: {out_paths_visited_ppy}")


if __name__ == "__main__":
    main()