import os
from loguru import logger
import sys
import math
logger.remove()
logger.add(sys.stdout, level="INFO")

def get_largest_rectangle(coords: list[list[int]]) -> int:
    length = len(coords)
    areas = []
    max_area = 0
    for i in range(length):
        row = []
        for j in range(length):
            if j < i:
                #compute area
                a = abs(coords[i][0] - coords[j][0])+1  # +1 because its inclusive
                b = abs(coords[i][1] - coords[j][1])+1
                area = a * b
                logger.debug(f"x:{coords[i][0]} y:{coords[i][1]}| x:{coords[j][0]} y:{coords[j][1]}| a:{a} | b {b} | area:{area}")
                if area > max_area:
                    max_area = area
                row.append(area)
        areas.append(row)
    for row in areas:
        logger.debug(row)
    return max_area


def get_bounds_x_y(coords: list[list[int]]):
    """
    Return bounds for each row and column
    """
    #fill the shape - connect points 
    all_points = []
    for i in range(0, len(coords)):
        #add points -1 and all points from coords -1 up to current
        all_points.append(coords[i-1])
        if coords[i-1][0] == coords[i][0]:
            range_x = range(1, abs(coords[i-1][1]-coords[i][1]))
            for j in range_x:
                #check if we go left or right
                if coords[i-1][1] > coords[i][1]:
                    all_points.append([coords[i][0], coords[i-1][1] - j])
                else:
                    all_points.append([coords[i][0], coords[i-1][1] + j])
        if coords[i-1][1] == coords[i][1]:
            range_y = range(1, abs(coords[i-1][0]-coords[i][0]))
            for j in range_y:
                #check if we go up/dow
                if coords[i-1][0] > coords[i][0]:
                    all_points.append([coords[i-1][0] - j, coords[i][1]])
                else:
                    all_points.append([coords[i-1][0] + j, coords[i][1]])
                
    bounds_x = {}
    bounds_y = {}
    for point in all_points:
        if point[1] not in bounds_x.keys():
            bounds_x[point[1]] = {}
            bounds_x[point[1]]["min"] = point[0]
            bounds_x[point[1]]["max"] = point[0]
        else:
            if point[0] < bounds_x[point[1]]["min"]:
                bounds_x[point[1]]["min"] = point[0]
            elif point[0] > bounds_x[point[1]]["max"]:
                bounds_x[point[1]]["max"] = point[0]
        if point[0] not in bounds_y.keys():
            bounds_y[point[0]] = {}
            bounds_y[point[0]]["min"] = point[1]
            bounds_y[point[0]]["max"] = point[1]
        else:
            if point[1] < bounds_y[point[0]]["min"]:
                bounds_y[point[0]]["min"] = point[1]
            elif point[1] > bounds_y[point[0]]["max"]:
                bounds_y[point[0]]["max"] = point[1]
    
    x_keys = list(bounds_x.keys())
    x_keys.sort()
    sorted_x_keys = {i: bounds_x[i] for i in x_keys}
    y_keys = list(bounds_y.keys())
    y_keys.sort()
    sorted_y_keys = {i: bounds_y[i] for i in y_keys}
    return sorted_x_keys, sorted_y_keys    
        

def rectangle_in_bounds(points: list[list[int]], bounds_x: dict, bounds_y: dict)-> bool:
    #check every point of rectangle frame
    # If we find at least one point out of bounds - return 0
    for k in range(0, len(points)):
        if points[k-1][0] == points[k][0]:
            range_x = range(abs(points[k-1][1]-points[k][1]))
            for l in range_x:
                #check if we go left or right
                if points[k-1][1] > points[k][1]:
                    x, y = points[k][0], points[k-1][1] - l
                else:
                    x, y = points[k][0], points[k-1][1] + l
                if x < bounds_x[y]["min"] or x > bounds_x[y]["max"]:
                    return False
                if y < bounds_y[x]["min"] or y > bounds_y[x]["max"]:
                    return False
        if points[k-1][1] == points[k][1]:
            range_y = range(abs(points[k-1][0]-points[k][0]))
            for l in range_y:
                #check if we go up/dow
                if points[k-1][0] > points[k][0]:
                    x, y = points[k-1][0] - l, points[k][1]
                else:
                    x, y = points[k-1][0] + l, points[k][1]
                if x < bounds_x[y]["min"] or x > bounds_x[y]["max"]:
                    return False
                if y < bounds_y[x]["min"] or y > bounds_y[x]["max"]:
                    return False
    return True


def task2_largest_rectangle(coords: list[list[int]]) -> int:
    bounds_x, bounds_y = get_bounds_x_y(coords=coords)
    length = len(coords)
    areas = []
    max_area = 0
    count_id = 0
    for i in range(length):
        row = []
        for j in range(i):
            logger.info(f"Total: {length**2 / 2} / {count_id} | Rectangle ID: {i} | {j}")
            count_id += 1
            points = [[coords[i][0], coords[i][1]], 
                      [coords[i][0], coords[j][1]], 
                      [coords[j][0], coords[j][1]], 
                      [coords[j][0], coords[i][1]]]
            
            #compute area if rectangle in shape
            if rectangle_in_bounds(points, bounds_x, bounds_y):
                a = abs(coords[i][0] - coords[j][0])+1  # +1 because its inclusive
                b = abs(coords[i][1] - coords[j][1])+1
                area = a * b
                # logger.debug(f"x:{coords[i][0]} y:{coords[i][1]}| x:{coords[j][0]} y:{coords[j][1]}| a:{a} | b {b} | area:{area}")
                if area > max_area:
                    max_area = area
                row.append(area)
        areas.append(row)
    for row in areas:
        logger.debug(row)
    return max_area


def main():
    task_input = None
    file_path = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(file_path, "input.txt"), "r") as f:
        task_input = f.readlines()
    
    task_input = [line.strip() for line in task_input]
    numbers = []
    for line in task_input:
        numbers.append([int(num) for num in line.split(",")])
    # logger.info(numbers)

    max_area = get_largest_rectangle(coords=numbers)
    logger.info(f"Task 1 result: {max_area}")   
    max_area_green_red = task2_largest_rectangle(coords=numbers)
    logger.info(f"Task 2 result: {max_area_green_red}")


if __name__ == "__main__":
    main()