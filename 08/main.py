import os
from loguru import logger
import sys
import math
import copy
from collections import defaultdict
logger.remove()
logger.add(sys.stdout, level="DEBUG")

CONNECTION_LIMIT = 1000

class Point:

    def __init__(self, x: int, y: int, z: int):
        self.x = x
        self.y = y
        self.z = z

    def get_distance(self, point2) -> float:
        euclids = (point2.x - self.x)**2 + (point2.y - self.y)**2 + (point2.z - self.z)**2
        dis = math.sqrt(euclids)
        return round(dis, 2)
    
    def is_in_circuit(self, points: list) -> bool:
        for point in points:
            if point.x == self.x and point.y == self.y and point.z == self.z:
                return True
        return False

    def __str__(self):
        return f"point: x: {self.x} | y: {self.y} | z: {self.z}"

class Pair:
    def __init__(self, id1: int, id2:int, distance: float):
        self.id1 = id1
        self.id2 = id2
        self.distance = distance

    def __str__(self):
        return f"Pair: xid1: {self.id1} | id2: {self.id2} | dist.: {self.distance}"

def sort_distances(distances: list[float]) -> list[Pair]:
    pairs = []
    for i in range(len(distances)):
        for j in range(len(distances[i])):
            pairs.append(Pair(i, j, distances[i][j]))

    pairs.sort(key=lambda x: x.distance)
    #delete those where IDs are same
    # new_pairs = []
    for pair in pairs:
        if pair.id1 == pair.id2:
            logger.debug(pair)
    return pairs

# def join_circuits(circuits) -> list[list[int]]:
#     # check if there are two boxes with same IDs: if yes, join them
#     merge_list = []
#     length = len(circuits)
#     for i in range(length):
        
#         for j in range(length):
#             if j < i:
#                 bool(set(circuits[i]) & set(circuits[j]))

#merge function to  merge all sublist having common elements.
#Took from https://www.geeksforgeeks.org/python/python-merge-list-with-common-elements-in-a-list-of-lists/
def merge_circuits(lists):
    neigh = defaultdict(set)
    visited = set()
    for each in lists:
        for item in each:
            neigh[item].update(each)
    def comp(node, neigh = neigh, visited = visited, vis = visited.add):
        nodes = set([node])
        next_node = nodes.pop
        while nodes:
            node = next_node()
            vis(node)
            nodes |= neigh[node] - visited
            yield node
    for node in neigh:
        if node not in visited:
            yield sorted(comp(node))


def wire_circuits(points: list[Point], distances: list[float]):
    sorted_pairs: list[Pair] = sort_distances(distances)
    circuits = []
    #put first circuit together
    circuits.append([sorted_pairs[0].id1, sorted_pairs[0].id2])
    for i in range(1, CONNECTION_LIMIT):
        point = sorted_pairs[i]
        #check arrys if IDs are there
        point_inserted = False
        point_in_circuits = []
        for j in range(len(circuits)):
            circuit = circuits[j]
            if point.id1 in circuit and point.id2 in circuit:   # both are there, skip whole logic and go to another point
                point_inserted = True
                break
            if point.id1 in circuit:
                circuit.append(point.id2)
                point_inserted = True
                point_in_circuits.append(j)
            elif point.id2 in circuit:
                circuit.append(point.id1)
                point_inserted = True
                point_in_circuits.append(j)
        
        #if points is in more that one circuits, merge those circuits togethert
        if len(point_in_circuits) > 1 :
            logger.info(f"point_in_circuits: {point_in_circuits}")
            index1, index2 = point_in_circuits[0], point_in_circuits[1]
            merged = list(set(circuits[index1]) | set(circuits[index2]))
            #remove index 2 and replace index2 with merged array
            del circuits[index2]
            circuits[index1] = merged
        if point_inserted == False:
            #create new circuit
            circuits.append([point.id1, point.id2])
    logger.debug(f"circuits: {circuits}")
    # multiply 3 biggest circuits
    circuit_sizes = [len(circuit) for circuit in circuits]
    
    circuit_sizes.sort(reverse=True)
    # logger.debug(f"circuit_sizes: {circuit_sizes}")
    result = 1
    logger.info(f"Top 3 circuits: {circuit_sizes[:3]}")
    for size in circuit_sizes[:3]:
        result *= size
    return result


def compute_distances(points: list[Point]):
    length = len(points)
    distances = []
    for i in range(length):
        row = []
        for j in range(length):
            if j < i:
                distance = points[j].get_distance(points[i])
                row.append(distance)
        distances.append(row)
    # for row in distances:
    #     logger.debug(row)
    return distances
        

def main():
    task_input = None
    file_path = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(file_path, "input.txt"), "r") as f:
        task_input = f.readlines()
    
    task_input = [string.strip().split(',') for string in task_input]
    logger.info(task_input)
    points = []
    for inp in task_input:
        points.append(Point(int(inp[0]), int(inp[1]), int(inp[2])))
    # for p in points:
    #     logger.debug(p)
    distances = compute_distances(points=points)
    result = wire_circuits(points=points, distances=copy.deepcopy(distances))
    logger.info(f"Result: {result}")


if __name__ == "__main__":
    main()