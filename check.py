from sys import argv
import sys
import networkx as nx
from axioms import axioms
import copy
import matplotlib.pyplot as plt
from math_strings import *

ax_choice = argv[1].split(",")
csv_file = argv[2]

with open(csv_file, "r") as f:
    csv_str = f.read()

csv_lines = csv_str.split("\n")

vertices = csv_lines[0].split("\t")[1::]
csv_lines = csv_lines[1::]

print()
print("*** VERTICES ***")
print(sstr(vertices))

transit_function = {}
ignore_tuples = []

for u in vertices:
    for v in vertices:
        transit_function[(u, v)] = set()
        if u == v:
            transit_function[(u, v)] = {u}

for line in csv_lines:
    if line == "":
        continue
    line = line.split("\t")
    source = line[0]
    line = line[1::]

    for i in range(len(line)):
        if line[i] == "x":
            continue
        elif line[i] == "":
            target = vertices[i]
            ignore_tuples += [(source, target)]
        else:
            target = vertices[i]
            if source == target:
                continue
            else:
                transit_list = line[i].split(",")
                transit_function[(source, target)] = set(transit_list)


for k in transit_function:
    curr_set = set(k)
    if transit_function[k] != set():
        if curr_set.issubset(transit_function[k]):
            continue
        else:
            print(r(k[0], k[1]), eq(), sstr(transit_function[k]))
            print("Last transit set violates (t1) or (t2).")
            sys.exit()

print("\n---\n")
print("*** Transit function before interval adding ***")

counter = 0

for k in transit_function:
    if counter % len(vertices) == 0 and counter != 0:
        print("-")
    print(r(k[0], k[1]), eq(), sstr(transit_function[k]))
    counter += 1

orig_transit_function = copy.copy(transit_function)

graph = nx.DiGraph()

for vert in vertices:
    graph.add_node(vert)

for k in transit_function:
    curr_set = set(k)
    if len(transit_function[k]) == 2:
        graph.add_edge(k[0], k[1])

print("\n---\n")
print("*** Constructed edges ***")
print(sstr(list(graph.edges())).replace("'",""))

added_paths = []

for k in transit_function:
    if k in ignore_tuples:
        continue
    curr_set = set(k)
    try:
        paths = list(nx.all_shortest_paths(graph, source=k[0], target=k[1]))
        # Change the last line to this one for the all-path function.
        # paths = list(nx.all_simple_paths(graph, source=k[0], target=k[1]))
    except nx.NetworkXNoPath:
        continue
    if len(paths) == 1:
        if len(paths[0]) == 1:
            continue
        if len(paths[0]) == 2:
            continue
    if transit_function[k] == set():
        t_set = set()
        for p in paths:
            t_set = t_set.union(set(p))
            added_paths += [k]
        transit_function[k] = t_set
    else:
        pass

print("\n---\n")
print("*** Transit function after interval adding ***")

for t in added_paths:
    print("Added path(s) for", str(t[0]).replace("'", ""), rarrow(), t[1].replace("'", ""))

if len(added_paths) > 0:
    print()

counter = 0
for k in transit_function:
    if counter % len(vertices) == 0 and counter != 0:
        print("-")
    print(r(k[0], k[1]), eq(), sstr(transit_function[k]))
    counter += 1

print("\n---\n")
print("*** Axiom checking ***")

ax = axioms(transit_function)
choice_string = str(ax_choice).replace("[", "").replace("]", "").replace("'","")

print("Checking the following axioms:", ax_choice, "\n")

if "t0" in ax_choice:
    print("Check t0...\n")
    for u in vertices:
        for v in vertices:
            for w in vertices:
                ax.t0(u, v, w)

if "t2s" in ax_choice:
    print("Check t2s...\n")
    for u in vertices:
        for v in vertices:
            ax.t2s(u, v)

if "t2a" in ax_choice:
    print("Check t2a...\n")
    for u in vertices:
        for v in vertices:
            ax.t2a(u, v)

if "b3" in ax_choice:
    print("Check b3...\n")
    for u in vertices:
        for x in vertices:
            for y in vertices:
                for v in vertices:
                    if x == v or u == y:
                        continue
                    else:
                        ax.b3_1(u, v, x, y)
                        ax.b3_2(u, v, x, y)

if "b5" in ax_choice:
    print("Check b5...\n")
    for u in vertices:
        for v in vertices:
            for w in vertices:
               ax.b5(u, v, w)

if "tr2" in ax_choice:
    print("Check tr2...\n")
    for u in vertices:
        for v in vertices:
            for w in vertices:
                ax.tr2(u, v, w)

if "b1" in ax_choice:
    print("Check b1...\n")
    for u in vertices:
        for v in vertices:
            for x in vertices:
                ax.b1_1(u, v, x)
                ax.b1_2(u, v, x)

if "b2" in ax_choice:
    print("Check b2...\n")
    for u in vertices:
        for v in vertices:
            for w in vertices:
                ax.b2(u, v, w)

if "b6" in ax_choice:
    print("Check b6...\n")
    for u in vertices:
        for v in vertices:
            for w in vertices:
                ax.b6_1(u, v, w)
                ax.b6_2(u, v, w)
                ax.b6_3(u, v, w)

if "j2" in ax_choice:
    print("Check j2...\n")
    for u in vertices:
        for v in vertices:
            for x in vertices:
                ax.j2(u, v, x)

if "med" in ax_choice:
    print("Check med...\n")
    for u in vertices:
        for w in vertices:
            for v in vertices:
                ax.med(u, v, w)

if "mod" in ax_choice:
    print("Check mod...\n")
    for u in vertices:
        for w in vertices:
            for v in vertices:
                ax.mod(u, v, w)

if "ta" in ax_choice:
    print("Check ta...\n")
    for u in vertices:
        for v in vertices:
            for w in vertices:
                ax.ta1(u, w, v)
                ax.ta2(u, w, v)

if "rv" in ax_choice:
    print("Check rv...\n")
    for u in vertices:
        for x in vertices:
            for y in vertices:
                for v in vertices:
                    if x == v or u == y:
                        continue
                    else:
                        ax.rv(u, x, y, v)

# TODO add missing axioms

# TODO order axioms

# TODO out-function cumbersome code

# TODO check wg and geometric

# TODO check graphic

# TODO check geodesic

# Drawing graph figure and saving it
nx.draw(graph, with_labels=True)
plt.savefig(csv_file.split(".")[0] + ".png")
print("\nG_R saved as", csv_file.split(".")[0] + ".png", "in working directory.\n")
