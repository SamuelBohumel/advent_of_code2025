import os
from typing import Tuple
from loguru import logger
import sys
logger.remove()
logger.add(sys.stdout, level="DEBUG")


class Range():
    
    def __init__(self, min: int, max: int):
        self.min = int(min)
        self.max = int(max)
        
    def __str__(self):
        return f"{self.min} {self.max}"    
    
    def is_num_in_range(self, ingredient_id: int) -> bool:
        return ingredient_id >= self.min and ingredient_id <= self.max


def handle_two_ranges(range1: Range, range2: Range) -> list:
    """_summary_
    Merge ranges if they overlap, if not, just return both of them.
    Args:
        range1 (Range): _description_
        range2 (Range): _description_
    """
    #from two same ranges return one:
    if range1.min == range2.min and range1.max == range2.max:
        return [range1]

    # if they dont overlap, return both | or if they exacly touch each other
    # Disjoint: r1 before r2
    if range1.max < range2.min:
        return [range1, range2]
    # Disjoint: r2 before r1
    elif range2.max < range1.min:
        return [range2, range1]

    #they exacly touch each other
    elif range1.max == range2.min:
        return [Range(min=range1.min, max=range2.max)]
    elif range2.max == range1.min:
        return [Range(min=range2.min, max=range1.max)]

    #overplap from one side (strict overlap)
    if not (range1.max < range2.min or range2.max < range1.min):
        # Merge any overlap or containment
        return [Range(min=min(range1.min, range2.min), max=max(range1.max, range2.max))]

    # range 1 wraps range 2
    elif range1.min <= range2.min and range1.max >= range2.max:
        return [range1]
    # range2 wraps range 1
    elif range2.min <= range1.min and range2.max >= range1.max:
        return [range2]

        
    


def get_total_fresh_ingredients_count(ranges: list[Range]) -> int:
    if not ranges:
        return 0

    ranges_sorted = sorted(ranges, key=lambda r: (r.min, r.max))

    merged: list[Range] = [ranges_sorted[0]]
    for r in ranges_sorted[1:]:
        last = merged[-1]
        result = handle_two_ranges(last, r)

        if len(result) == 1:
            # Overlap or touch -> merged into a single range
            merged[-1] = result[0]
        else:
            # Disjoint -> append the next range
            # Because we sorted, result should be [last, r] in order
            merged.append(r)
        

    total = sum(r.max - r.min for r in merged)
    return int(total)

            


def main():
    task_input = None
    file_path = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(file_path, "input.txt"), "r") as f:
        task_input = f.readlines()
    
    
    #clear from newlines 
    task_input = [number.strip() for number in task_input]
    # logger.info(task_input)
    empty_str_index = -1
    for i, number in enumerate(task_input):
        if number == '':
            empty_str_index = i
    assert empty_str_index != -1
    
    ranges_str = task_input[:empty_str_index]
    ingredients_to_check = task_input[empty_str_index+1:]
    # logger.debug(f"ranges: {ranges_str}")
    # logger.debug(f"ingredients: {ingredients_to_check}")
    
    #create arrays of ranges 
    ranges = []
    for item in ranges_str:
        ranges.append(
            Range(min=item.split('-')[0], 
                  max=item.split('-')[1]))
    #task 2
    total_ingr = get_total_fresh_ingredients_count(ranges)
    logger.info(f"Total ingr: {total_ingr}")
    
    #task 1
    #check if every ingredient is in range
    # fresh_ingr = 0
    # for ingredient_id in ingredients_to_check:
    #     exist_check = [range_item.is_num_in_range(int(ingredient_id)) for range_item in ranges]
    #     if any(exist_check):
    #         fresh_ingr += 1
            
    # logger.info(f"Fresh ingredients count: {fresh_ingr}")
    # get_total_fresh_ingredients_count(ranges)
    # all_possible_ids = get_total_fresh_ingredients_count(ranges_str)
    # logger.info(f"all_possible_ids: {all_possible_ids}")


if __name__ == "__main__":
    main()