from loguru import logger

#Importing 
from collections import defaultdict

#merge function to  merge all sublist having common elements.
def merge_common(lists):
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

def join_circuits(circuits) -> list[list[int]]:
    # check if there are two boxes with same IDs: if yes, join them
    merge_list = []
    length = len(circuits)
    for i in range(length):
        merged = False
        for j in range(length):
            if j < i:
                logger.info(f"{circuits[i]} | {circuits[j]}: {bool(set(circuits[i]) & set(circuits[j]))}")  
                if bool(set(circuits[i]) & set(circuits[j])):
                    merge_list.append(list(set(circuits[i]) | set(circuits[j])))
                    merged = True
        if merged == False:
            merge_list.append(circuits[i])
        
    logger.debug(merge_list)
circuits = [[19, 0, 7, 14], [13, 2, 8, 18], [18, 17], [12, 9], [16, 11]]

join_circuits(circuits)
circuits = merge_common(circuits)
logger.info(type(list(circuits)))
for cir in circuits:
    logger.info(cir)