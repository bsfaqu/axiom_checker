from sys import argv
import sys
import networkx as nx
from axioms import axioms
import copy
import matplotlib.pyplot as plt
from math_strings import *

# Parse command-line arguments.
ax_choice = argv[1].split(",")
csv_file = argv[2]

# Read input file
with open(csv_file, "r") as f:
    csv_str = f.read()

# Get the lines
csv_lines = csv_str.split("\n")

# Parse vertices from the first line
vertices = csv_lines[0].split("\t")[1::]

# Remove the first line (only contains vertices)
csv_lines = csv_lines[1::]

# Output vertices for sanity checking
print()
print("*** VERTICES ***")
print(sstr(vertices))

# Here we save all the transit sets. Keys are tuples (u,v) and values are sets.
transit_function = {}

# Transit sets that are always supposed to be empty, i.e fields filled
# with "", hence no string
ignore_tuples = []

# Initialize transit sets as empty and ensure (t3)
for u in vertices:
    for v in vertices:
        transit_function[(u, v)] = set()

        # Enforce (t3)
        if u == v:
            transit_function[(u, v)] = {u}

# Parse all the transit sets supplied in the .tsv
for line in csv_lines:

    # Last line
    if line == "":
        continue

    # Split line by tabulators. First field is always the source.
    line = line.split("\t")
    source = line[0]

    # Split line by tabulator. Now every list entry in the line
    # is lined up with the vertices in vertices.
    line = line[1::]


    # Iterate over line and fill the transit function.
    for i in range(len(line)):

        # This is ensured by (t3) already, or this will be
        # substituted with the shortest path(s) in G_R later.
        if line[i] == "x":
            continue

        # ignore line, hence this transit set is kept empty
        elif line[i] == "":
            target = vertices[i]

            # Keep track of purposefully emptpy sets
            ignore_tuples += [(source, target)]
        else:
            # Set transit sets in transit_function. R(u,u) entries are ignored.
            target = vertices[i]
            if source == target:
                continue
            else:
                transit_list = line[i].split(",")
                transit_function[(source, target)] = set(transit_list)


# Check of (t1)
for k in transit_function:
    curr_set = set(k)
    if transit_function[k] != set():
        if curr_set.issubset(transit_function[k]):
            continue
        else:
            print(r(k[0], k[1]), eq(), sstr(transit_function[k]))
            print("Last transit set violates (t1) or (t3).")
            sys.exit()

# Output supplied transit sets
print("\n---\n")
print("*** Transit function before interval adding ***")

counter = 0

for k in transit_function:
    if counter % len(vertices) == 0 and counter != 0:
        print("-")
    print(r(k[0], k[1]), eq(), sstr(transit_function[k]))
    counter += 1

# Save the original transit function
orig_transit_function = copy.copy(transit_function)

# Initialize NetworkX graph object to obtain shortest paths later
graph = nx.DiGraph()

# Add all the vertices
for vert in vertices:
    graph.add_node(vert)

# Add all the edges (defined by transit sets of size 2)
for k in transit_function:
    curr_set = set(k)
    if len(transit_function[k]) == 2:
        graph.add_edge(k[0], k[1])

# Output edges of G_R
print("\n---\n")
print("*** Constructed edges ***")
print(sstr(list(graph.edges())).replace("'",""))

# Keep track of added paths
added_paths = []

for k in transit_function:
    # If the transit set R(k[0], k[1]) should be kept empty,
    # also transit sets for R(u, u) are ignored
    if k in ignore_tuples or k[0] == k[1]:
        continue

    # Get all the shortest paths with nx
    try:
        paths = list(nx.all_shortest_paths(graph, source=k[0], target=k[1]))
        # Change the last line to this one for the all-path function.
        # paths = list(nx.all_simple_paths(graph, source=k[0], target=k[1]))
    except nx.NetworkXNoPath:
        continue

    # Is there only one path
    if len(paths) == 1:
        # Does the path only contain one vertex (u = v), continue.
        if len(paths[0]) == 1:
            continue
        # Does the path contain two vertices (edge must be defined as such already), continue
        if len(paths[0]) == 2:
            continue

    # If the transit set for this tuple is not set yet (not supplied by user)
    if transit_function[k] == set():
        t_set = set()

        # Collecting all vertices along all shortest paths in t_set
        for p in paths:
            t_set = t_set.union(set(p))
            added_paths += [k]

        # Set the transit set of current tuple to t_set
        transit_function[k] = t_set
    else:
        pass

# Output the transit function after adding the shortest paths in G_R
print("\n---\n")
print("*** Transit function after interval adding ***")

# output the added paths
for t in added_paths:
    print("Added path(s) for", str(t[0]).replace("'", ""), rarrow(), t[1].replace("'", ""))

if len(added_paths) > 0:
    print()

# Provide a structured output of the transit function
counter = 0
for k in transit_function:
    if counter % len(vertices) == 0 and counter != 0:
        print("-")
    print(r(k[0], k[1]), eq(), sstr(transit_function[k]))
    counter += 1

# Axiom checking output
print("\n---\n")
print("*** Axiom checking ***")

# Initialize axiom object
ax = axioms(transit_function)

# Output which axioms are checked
choice_string = str(ax_choice).replace("[", "").replace("]", "").replace("'","")
print("Checking the following axioms:", ax_choice, "\n")

# Initialize dictionary to save which axioms are satisfied
sat_axioms = dict()
for a in ax_choice:
    if a in ["b1", "b2"]:
        sat_axioms[a] = [True, True]
    elif a in ["b6"]:
        sat_axioms[a] = [True, True, True]
    else:
        sat_axioms[a] = True

# Check all the axioms.

if "t0" in ax_choice:
    print("Check t0...\n")
    for u in vertices:
        for v in vertices:
            for w in vertices:
                sat_val = ax.t0(u, v, w)

if "t2s" in ax_choice:
    print("Check t2s...\n")
    for u in vertices:
        for v in vertices:
            sat_val = ax.t2s(u, v)

if "t2a" in ax_choice:
    print("Check t2a...\n")
    for u in vertices:
        for v in vertices:
            sat_val = ax.t2a(u, v)

if "tr2" in ax_choice:
    print("Check tr2...\n")
    for u in vertices:
        for v in vertices:
            for w in vertices:
                sat_val = ax.tr2(u, v, w)

if "b1" in ax_choice:
    print("Check b1...\n")
    for u in vertices:
        for v in vertices:
            for x in vertices:
                sat_val_1 = ax.b1_1(u, v, x)
                sat_val_2 = ax.b1_2(u, v, x)

if "b2" in ax_choice:
    print("Check b2...\n")
    for u in vertices:
        for v in vertices:
            for w in vertices:
                sat_val = ax.b2(u, v, w)

if "b3" in ax_choice:
    print("Check b3...\n")
    for u in vertices:
        for x in vertices:
            for y in vertices:
                for v in vertices:
                    if x == v or u == y:
                        continue
                    else:
                        sat_val_1 = ax.b3_1(u, v, x, y)
                        sat_val_2 = ax.b3_2(u, v, x, y)

if "b4" in ax_choice:
    print("Check b4...\n")
    for u in vertices:
        for v in vertices:
            for x in vertices:
               ax.b4(u, v, x)

if "b6" in ax_choice:
    print("Check b6...\n")
    for u in vertices:
        for v in vertices:
            for w in vertices:
                sat_val_1 = ax.b6_1(u, v, w)
                sat_val_2 = ax.b6_2(u, v, w)
                sat_val_3 = ax.b6_3(u, v, w)

if "j2" in ax_choice:
    print("Check j2...\n")
    for u in vertices:
        for v in vertices:
            for x in vertices:
                sat_val = ax.j2(u, v, x)

if "F" in ax_choice:
    print("Check F...\n")
    for u in vertices:
        for v in vertices:
            for x in vertices:
                for y in vertices:
                    sat_val = ax.F(u, v, x, y)

if "G" in ax_choice:
    print("Check G...\n")
    for u in vertices:
        for v in vertices:
            for x in vertices:
                for y in vertices:
                    sat_val = ax.G(u, v, x, y)

if "co0" in ax_choice:
    print("Check co0...\n")
    for u in vertices:
        for v in vertices:
            for x in vertices:
                sat_val = ax.co0(u, v, x)

if "co1" in ax_choice:
    print("Check co1...\n")
    for u in vertices:
        for v in vertices:
            for x in vertices:
                sat_val = ax.co1(u, v, x)

if "co2" in ax_choice:
    print("Check co2...\n")
    for u in vertices:
        for v in vertices:
            for x in vertices:
                for y in vertices:
                    sat_val = ax.co2(u, v, x, y)

if "co3" in ax_choice:
    print("Check co3...\n")
    for u in vertices:
        for v in vertices:
            for x in vertices:
                for y in vertices:
                    sat_val = ax.co3(u, v, x, y)

if "g" in ax_choice:
    print("Check g...\n")
    for u in vertices:
        for v in vertices:
            for x in vertices:
                for y in vertices:
                    sat_val = ax.g(u, v, x, y)

if "p" in ax_choice:
    print("Check p...\n")
    for u in vertices:
        for v in vertices:
            for x in vertices:
                sat_val = ax.p(u, v, x)

if "mod" in ax_choice:
    print("Check mod...\n")
    for u in vertices:
        for w in vertices:
            for v in vertices:
                sat_val = ax.mod(u, v, w)

if "med" in ax_choice:
    print("Check med...\n")
    for u in vertices:
        for w in vertices:
            for v in vertices:
                sat_val = ax.med(u, v, w)

if "b5" in ax_choice:
    print("Check b5...\n")
    for u in vertices:
        for v in vertices:
            for w in vertices:
               sat_val = ax.b5(u, v, w)

if "ta" in ax_choice:
    print("Check ta...\n")
    for u in vertices:
        for v in vertices:
            for w in vertices:
                sat_val_1 = ax.ta1(u, w, v)
                sat_val_2 = ax.ta2(u, w, v)

if "rv" in ax_choice:
    print("Check rv...\n")
    for u in vertices:
        for x in vertices:
            for y in vertices:
                for v in vertices:
                    if x == v or u == y:
                        continue
                    else:
                        sat_val = ax.rv(u, x, y, v)

# Initialize some vars for graphic check
is_graphic = True
graphic_violating_sets = dict()

# Compare each transit set to the interval function of G_R
for k in transit_function:
    curr_transit_set = transit_function[k]

    # Get all shortest paths
    try:
        paths = list(nx.all_shortest_paths(graph, source=k[0], target=k[1]))
    except nx.NetworkXNoPath:
        continue

    path_curr_set = set()

    # Add all vertices along shortest path to set
    for path in paths:
        path_curr_set.update(set(path))

    # Compare I_{G_R}(u, v) with R(u,v)
    if path_curr_set != curr_transit_set:
        is_graphic = False
        graphic_violating_sets[k] = path_curr_set


# Output if R is graphic
if is_graphic:
    print("Given transit function is graphic, hence R=I_{G_R}.")
# In the negative case also output the violating pairs
else:
    print("Given transit function is NOT graphic as R",neq(), "I_{G_R}.")
    print("Violating transit sets:")
    for k in graphic_violating_sets:
        print(r(k[0], k[1]), " ", eq(), " ", sstr(transit_function[k]), " ", neq(), " ",
              sstr(graphic_violating_sets[k]), " ", eq(), " I(",
              str(k[0]).replace("'", ""), ",", str(k[1]).replace("'", ""), ")", sep="")
    print()


# Drawing graph figure and saving it
nx.draw(graph, with_labels=True)
plt.savefig(csv_file.split(".")[0] + ".png")
print("\nG_R saved as", csv_file.split(".")[0] + ".png", "in working directory.\n")
