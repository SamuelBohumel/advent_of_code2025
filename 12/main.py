import os
from loguru import logger
import sys
logger.remove()
logger.add(sys.stdout, level="DEBUG")

PRESENT_UNIT = "#"
SPACE_UNIT = '.'

class Present:
    
    def __init__(self, shape: list[str]):
        self.shape = shape
        counter = 0
        for line in shape:
            counter += line.count(PRESENT_UNIT)
        self.shape_area = counter
        
class Tree:
    
    def __init__(self, tree_desc: str):
        dimensions, presents = tree_desc.split(": ")
        self.width, self.height = dimensions.split('x')
        self.area = int(self.width) * int(self.height)
        self.presents = [int(present_id) for present_id in presents.split(" ")]
        
        
    def presents_fit(self, presents: list[Present]) -> bool:
        logger.debug(f"Total area: {self.area}")
        presents_area = 0
        for i, present_count in enumerate(self.presents):
            if present_count > 0:
                # logger.debug(f"{i}: present count: {present_count}")
                presents_area += (presents[i].shape_area * present_count)
                
        logger.info(f"Tree area: {self.area} | presents_area: {presents_area}")
            
        if presents_area > self.area:
            return False
        return True


def main():
    task_input = None
    file_path = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(file_path, "input.txt"), "r") as f:
        task_input = f.readlines()
        task_input = [row.strip() for row in task_input]
    
    presents = []
    trees = []
    present = []
    for line in task_input[1:]:
        if ":" in line and "x" not in line:
            presents.append(present)
            present = []
        elif "#"  in line or "." in line:
            present.append(line)
        if "x" in line and ":" in line:
            trees.append(line) 
    presents.append(present)
    logger.info(presents)
    logger.info(trees)
    presents = [Present(pres) for pres in presents]
    trees = [Tree(tree_desc) for tree_desc in trees]
    
    count_task1 = 0
    for tree in trees:
        if tree.presents_fit(presents):
            count_task1 += 1
            
    logger.info(f"Trees that fit their presents: {count_task1}")


if __name__ == "__main__":
    main()