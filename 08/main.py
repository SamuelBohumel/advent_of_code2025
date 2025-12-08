import os
from loguru import logger
import sys
import math
import copy
logger.remove()
logger.add(sys.stdout, level="DEBUG")

CONNECTION_LIMIT = 10

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
    # for pair in pairs:
    #     if pair.id1 == pair.id2:
    #         logger.debug(pair)
    #     else:
    #         new_pairs.append(pair)
    return pairs


def wire_circuits(points: list[Point], distances: list[float]):
    sorted_pairs: list[Pair] = sort_distances(distances)
    circuits = []
    #put first circuit together
    circuits.append([sorted_pairs[0].id1, sorted_pairs[0].id2])
    counter = 1
    for point in sorted_pairs:
        if counter == CONNECTION_LIMIT:
            break
        #check arrys if IDs are there
        point_inserted = False
        for circuit in circuits:
            if point.id1 in circuit and point.id2 in circuit:   # both are there, skip
                point_inserted = True
                break
            if point.id1 in circuit:
                circuit.append(point.id2)
                counter += 1
                point_inserted = True
            elif point.id2 in circuit:
                circuit.append(point.id1)
                counter += 1
                point_inserted = True
        if point_inserted == False:
            #create new circuit
            circuits.append([point.id1, point.id2])
            counter += 1
    # multiply 3 biggest circuits
    circuit_sizes = [len(circuit) for circuit in circuits]
    logger.debug(f"circuit_sizes: {circuit_sizes}")
    circuit_sizes.sort(reverse=True)
    result = 1
    for size in circuit_sizes[:3]:
        result *= size
    return result


def compute_distances(points: list[Point]):
    length = len(points)
    distances = []
    for i in range(length):
        row = []
        if i == 0:
            continue
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
    with open(os.path.join(file_path, "ex_input.txt"), "r") as f:
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