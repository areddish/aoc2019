class Node:
    def __init__(self, name, prev):
        self.name = name
        self.prev = prev
        
    def __str__(self):
        return "{} <-- {}".format(self.name,self.prev.name if self.prev else "")

def get_path(nodes, target, target_parent_name="COM"):
    my_path = []
    dist = 0
    parent = nodes[target].prev
    if parent:    
        my_path.append(parent.name)
        dist += 1
    while parent and parent.name != target_parent_name:
        parent = parent.prev         
        if parent:
            my_path.append(parent.name)
            dist += 1
   
    return my_path, dist

import time
start = time.time()
root = None
nodes = {}
nodes["COM"] = Node("COM", None)

#with open("test.txt") as file:
with open("input.txt") as file:
    for line in file:
        inner, outer = line.strip().split(")")

        # inner <-- outer        
        inner_node = nodes.get(inner, Node(inner, None))
        nodes[inner] = inner_node
        outer_node = nodes.get(outer, Node(outer, inner_node))
        assert outer_node.prev == None or outer_node.prev == inner_node
        outer_node.prev = inner_node
        nodes[outer] = outer_node

count = 0
for name in nodes:
    path, dist = get_path(nodes, name)
    count += dist

print(f"Part 1: {count} {time.time()-start}")

start = time.time()

node_before_you = nodes["YOU"].prev
node_before_santa = nodes["SAN"].prev

my_path, _ = get_path(nodes, node_before_you.name)
santa_path, _ = get_path(nodes, node_before_santa.name)
common_points = set(my_path)&set(santa_path)

santa_distances = len(nodes)
my_distances = santa_distances
for pt in common_points:
    santa_distances = min(santa_distances, get_path(nodes,node_before_santa.name,pt)[1])
    my_distances = min(my_distances, get_path(nodes,node_before_you.name,pt)[1])

print(f"Part 2: {santa_distances+my_distances} {time.time()-start}")
