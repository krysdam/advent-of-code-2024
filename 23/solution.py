from collections import defaultdict

# Read the graph from the file,
# as a dict from each node to a list of its neighbors.
graph = defaultdict(list)
with open('input.txt', 'r') as f:
    for line in f:
        line = line.strip()
        comp1, comp2 = line.split('-')
        graph[comp1].append(comp2)
        graph[comp2].append(comp1)

def all_three_cliques(graph):
    """Return a set of all 3-member cliques of the graph."""
    cliques = set()
    for node1 in graph:
        for neighbor1 in graph[node1]:
            for neighbor2 in graph[node1]:
                if neighbor2 in graph[neighbor1]:
                    clique = tuple(sorted([node1, neighbor1, neighbor2]))
                    cliques.add(clique)
    return cliques

def has_tcomputer(computers):
    """Does one of the computers start with 't'?"""
    has = False
    for computer in computers:
        if computer[0] == 't':
            has = True
    return has


# Part 1: How many 3-cliques with a computer that starts with t?

three_cliques = all_three_cliques(graph)
candidates = [clique for clique in three_cliques if has_tcomputer(clique)]
print(f'Part 1: {len(candidates)}')


# Part 2: Members of the largest clique.
# By inspection, each computer has exactly 13 connections.
# So the largest possible clique would have 14 members.
# So we can just check if there's a clique of 14 members,
# and if not, if there's a clique of 13 members,
# and if not, and so on, and hopefully, we'll find one soon.

def clique_to_string(nodes):
    """Format the clique in the desired way (alphabetical, comma-separated)."""
    nodes = sorted(nodes)
    return ','.join(nodes)

def is_clique(graph, nodes):
    """Are the nodes a clique of the graph (all mutually connected)?"""
    for node1 in nodes:
        for node2 in nodes:
            if node1 == node2:
                continue
            if node1 not in graph[node2]:
                return False
    return True

# Hypothesis 1: There is a clique of 14 members.
# This would mean that a single node's neighbor set is a clique
# (plus the node itself connected to them all makes a clique of 14).

for node in graph:
    candidate = graph[node]
    if is_clique(graph, candidate):
        clique = [node] + candidate
        print(f'Part 2: {clique_to_string(clique)}')
        exit()

# Prints nothing. There are no cliques of 14 members.

# Hypothesis 2: There is a clique of 13 members.
# This would mean that for some node, all but one of its neighbors are a clique.

for node in graph:
    neighbors = graph[node]
    for i in range(len(neighbors)):
        candidate = neighbors[:i] + neighbors[i+1:]
        if is_clique(graph, candidate):
            clique = [node] + candidate
            print(f'Part 2: {clique_to_string(clique)}')
            exit()

# Prints our clique.