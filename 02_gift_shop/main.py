import os
from loguru import logger
import sys
logger.remove()
logger.add(sys.stdout, level="INFO")

def array_has_same_items(arr: list) -> bool:
    if len(arr) == 0 or len(arr) == 1:
        return True
    first = arr[0]
    for item in arr:
        if first != item:
            return False
    return True
        

def is_id_valid(id: int) -> bool:
    #retrun false from numbers with odd length
    length =  len(str(id))
     
    for dividor in range(1, length):
        #check if number is divisible by this
        array = []
        if length % dividor == 0:
            logger.debug(f"  id: {id} | length: {length} | dividor: {dividor}")
            for j in range(0, length, dividor):   
                array.append(str(id)[j:j+dividor])
            logger.debug(f" {array}")
            if array_has_same_items(array):
                return True
    return False


def main():
    task_input = None
    file_path = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(file_path, "input.txt"), "r") as f:
        task_input = f.readlines()
    
    invalid_ids = []
    task_input = task_input[0]
    # logger.info(task_input)
    id_ranges = task_input.split(',')
    for id_range in id_ranges:
        logger.info(id_range)
        bottom = int(id_range.split('-')[0])
        limit = int(id_range.split('-')[1]) + 1
        #iterate range
        for i in range(bottom, limit):
            if is_id_valid(i):
                logger.debug(f" number: {i}, | {is_id_valid(i)}")
                invalid_ids.append(i)
    
    added_invalid_ids = sum(invalid_ids)
    logger.info(f"All invalid IDs: {invalid_ids}")
    logger.info(f"Sum: {added_invalid_ids}")


if __name__ == "__main__":
    main()