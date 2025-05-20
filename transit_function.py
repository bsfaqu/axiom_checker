from sys import argv
import sys
import networkx as nx
from tf_axioms import axioms
import copy
import matplotlib.pyplot as plt
from math_strings import *

class transit_function:

    transit_function = {}
    axioms = None
    graph = None
    vertices = None

    # TODO add optional output (print_info = True or sth similar)

    def __init__(self, csv_lines):
        # Parse vertices from the first line
        vertices = csv_lines[0].split("\t")[1::]

        # Remove the first line (only contains vertices)
        csv_lines = csv_lines[1::]

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
                if line[i] == "*":
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
        print(sstr(list(graph.edges())).replace("'", ""))

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

        # Store transit function in class variable
        self.transit_function = transit_function

        # Initialize axioms with transit function and save in class variable
        self.axioms = axioms(self.transit_function)

        # Save digraph to class variable
        self.graph = graph

        self.vertices = vertices

    def R(self, u, v):
        return sstr(self.transit_function[(u, v)])

    def check_axioms(self, ax_choice, print_info=True):

        # Potential strings to pick axioms:
        # axiom_strings_transit = [
        #     "t0", "t1", "t2s", "t2a", "t3",
        #     "tr2", "b1", "b2", "b3", "b4",
        #     "b6", "j2", "F", "G", "co0",
        #     "co1", "co2", "co3", "g", "p",
        #     "mod", "med", "b5"
        # ]

        # TODO Change namespace to .self for vertices
        vertices = self.vertices

        # Initialize dictionary to save which axioms are satisfied
        # sat_axioms = dict()
        # for a in ax_choice:
        #     if a in ["b1", "b2"]:
        #         sat_axioms[a] = [True, True]
        #     elif a in ["b6"]:
        #         sat_axioms[a] = [True, True, True]
        #     else:
        #         sat_axioms[a] = True

        sat_list = [False for a in ax_choice]

        # Check all the axioms.

        if "t0" in ax_choice:
            print("Check t0...\n")
            for u in vertices:
                for v in vertices:
                    for w in vertices:
                        sat_val = self.axioms.t0(u, v, w, print_info=print_info)
                        sat_list[ax_choice.index("t0")] = min(sat_list[ax_choice.index("t0")], sat_val)

        if "t2s" in ax_choice:
            print("Check t2s...\n")
            for u in vertices:
                for v in vertices:
                    sat_val = self.axioms.t2s(u, v, print_info=print_info)
                    sat_list[ax_choice.index("t2s")] = min(sat_list[ax_choice.index("t2s")], sat_val)

        if "t2a" in ax_choice:
            print("Check t2a...\n")
            for u in vertices:
                for v in vertices:
                    sat_val = self.axioms.t2a(u, v, print_info=print_info)
                    sat_list[ax_choice.index("t2a")] = min(sat_list[ax_choice.index("t2a")], sat_val)

        if "tr2" in ax_choice:
            print("Check tr2...\n")
            for u in vertices:
                for v in vertices:
                    for w in vertices:
                        sat_val = self.axioms.tr2(u, v, w, print_info=print_info)
                        sat_list[ax_choice.index("tr2")] = min(sat_list[ax_choice.index("tr2")], sat_val)

        if "b1" in ax_choice:
            print("Check b1...\n")
            for u in vertices:
                for v in vertices:
                    for x in vertices:
                        sat_val_1 = self.axioms.b1_1(u, v, x, print_info=print_info)
                        sat_list[ax_choice.index("b1")] = min(sat_list[ax_choice.index("b1")], sat_val)
                        sat_val_2 = self.axioms.b1_2(u, v, x, print_info=print_info)
                        sat_list[ax_choice.index("b1")] = min(sat_list[ax_choice.index("b1")], sat_val)

        if "b2" in ax_choice:
            print("Check b2...\n")
            for u in vertices:
                for v in vertices:
                    for w in vertices:
                        sat_val = self.axioms.b2(u, v, w, print_info=print_info)
                        sat_list[ax_choice.index("b2")] = min(sat_list[ax_choice.index("b2")], sat_val)

        if "b3" in ax_choice:
            print("Check b3...\n")
            for u in vertices:
                for x in vertices:
                    for y in vertices:
                        for v in vertices:
                            if x == v or u == y:
                                continue
                            else:
                                sat_val_1 = self.axioms.b3_1(u, v, x, y, print_info=print_info)
                                sat_list[ax_choice.index("b3")] = min(sat_list[ax_choice.index("b3")], sat_val)
                                sat_val_2 = self.axioms.b3_2(u, v, x, y, print_info=print_info)
                                sat_list[ax_choice.index("b3")] = min(sat_list[ax_choice.index("b3")], sat_val)

        if "b4" in ax_choice:
            print("Check b4...\n")
            for u in vertices:
                for v in vertices:
                    for x in vertices:
                        self.axioms.b4(u, v, x, print_info=print_info)
                        sat_list[ax_choice.index("b4")] = min(sat_list[ax_choice.index("b4")], sat_val)

        if "b6" in ax_choice:
            print("Check b6...\n")
            for u in vertices:
                for v in vertices:
                    for w in vertices:
                        sat_val_1 = self.axioms.b6_1(u, v, w, print_info=print_info)
                        sat_list[ax_choice.index("b6")] = min(sat_list[ax_choice.index("b6")], sat_val)
                        sat_val_2 = self.axioms.b6_2(u, v, w, print_info=print_info)
                        sat_list[ax_choice.index("b6")] = min(sat_list[ax_choice.index("b6")], sat_val)
                        sat_val_3 = self.axioms.b6_3(u, v, w, print_info=print_info)
                        sat_list[ax_choice.index("b6")] = min(sat_list[ax_choice.index("b6")], sat_val)

        if "j2" in ax_choice:
            print("Check j2...\n")
            for u in vertices:
                for v in vertices:
                    for x in vertices:
                        sat_val = self.axioms.j2(u, v, x, print_info=print_info)
                        sat_list[ax_choice.index("j2")] = min(sat_list[ax_choice.index("j2")], sat_val)

        if "F" in ax_choice:
            print("Check F...\n")
            for u in vertices:
                for v in vertices:
                    for x in vertices:
                        for y in vertices:
                            sat_val = self.axioms.F(u, v, x, y, print_info=print_info)
                            sat_list[ax_choice.index("F")] = min(sat_list[ax_choice.index("F")], sat_val)

        if "G" in ax_choice:
            print("Check G...\n")
            for u in vertices:
                for v in vertices:
                    for x in vertices:
                        for y in vertices:
                            sat_val = self.axioms.G(u, v, x, y, print_info=print_info)
                            sat_list[ax_choice.index("G")] = min(sat_list[ax_choice.index("G")], sat_val)

        if "co0" in ax_choice:
            print("Check co0...\n")
            for u in vertices:
                for v in vertices:
                    for x in vertices:
                        sat_val = self.axioms.co0(u, v, x, print_info=print_info)
                        sat_list[ax_choice.index("co0")] = min(sat_list[ax_choice.index("co0")], sat_val)

        if "co1" in ax_choice:
            print("Check co1...\n")
            for u in vertices:
                for v in vertices:
                    for x in vertices:
                        sat_val = self.axioms.co1(u, v, x, print_info=print_info)
                        sat_list[ax_choice.index("co1")] = min(sat_list[ax_choice.index("co1")], sat_val)

        if "co2" in ax_choice:
            print("Check co2...\n")
            for u in vertices:
                for v in vertices:
                    for x in vertices:
                        for y in vertices:
                            sat_val = self.axioms.co2(u, v, x, y, print_info=print_info)
                            sat_list[ax_choice.index("co2")] = min(sat_list[ax_choice.index("co2")], sat_val)

        if "co3" in ax_choice:
            print("Check co3...\n")
            for u in vertices:
                for v in vertices:
                    for x in vertices:
                        for y in vertices:
                            sat_val = self.axioms.co3(u, v, x, y, print_info=print_info)
                            sat_list[ax_choice.index("co3")] = min(sat_list[ax_choice.index("co3")], sat_val)

        if "g" in ax_choice:
            print("Check g...\n")
            for u in vertices:
                for v in vertices:
                    for x in vertices:
                        for y in vertices:
                            sat_val = self.axioms.g(u, v, x, y, print_info=print_info)
                            sat_list[ax_choice.index("g")] = min(sat_list[ax_choice.index("g")], sat_val)

        if "p" in ax_choice:
            print("Check p...\n")
            for u in vertices:
                for v in vertices:
                    for x in vertices:
                        sat_val = self.axioms.p(u, v, x, print_info=print_info)
                        sat_list[ax_choice.index("p")] = min(sat_list[ax_choice.index("p")], sat_val)

        if "mod" in ax_choice:
            print("Check mod...\n")
            for u in vertices:
                for w in vertices:
                    for v in vertices:
                        sat_val = self.axioms.mod(u, v, w, print_info=print_info)
                        sat_list[ax_choice.index("mod")] = min(sat_list[ax_choice.index("mod")], sat_val)

        if "med" in ax_choice:
            print("Check med...\n")
            for u in vertices:
                for w in vertices:
                    for v in vertices:
                        sat_val = self.axioms.med(u, v, w, print_info=print_info)
                        sat_list[ax_choice.index("med")] = min(sat_list[ax_choice.index("med")], sat_val)

        if "b5" in ax_choice:
            print("Check b5...\n")
            for u in vertices:
                for v in vertices:
                    for w in vertices:
                        sat_val = self.axioms.b5(u, v, w, print_info=print_info)
                        sat_list[ax_choice.index("b5")] = min(sat_list[ax_choice.index("b5")], sat_val)

        if "ta" in ax_choice:
            print("Check ta...\n")
            for u in vertices:
                for v in vertices:
                    for w in vertices:
                        sat_val_1 = self.axioms.ta1(u, w, v, print_info=print_info)
                        sat_list[ax_choice.index("ta")] = min(sat_list[ax_choice.index("ta")], sat_val)
                        sat_val_2 = self.axioms.ta2(u, w, v, print_info=print_info)
                        sat_list[ax_choice.index("ta")] = min(sat_list[ax_choice.index("ta")], sat_val)

        if "rv" in ax_choice:
            print("Check rv...\n")
            for u in vertices:
                for x in vertices:
                    for y in vertices:
                        for v in vertices:
                            if x == v or u == y:
                                continue
                            else:
                                sat_val = self.axioms.rv(u, x, y, v, print_info=print_info)
                                sat_list[ax_choice.index("rv")] = min(sat_list[ax_choice.index("rv")], sat_val)

        return sat_list

    def check_additional(self):

        # Initialize some vars for graphic check
        is_graphic = True
        graphic_violating_sets = dict()

        # Compare each transit set to the interval function of G_R
        for k in self.transit_function:
            curr_transit_set = self.transit_function[k]

            # Get all shortest paths
            try:
                paths = list(nx.all_shortest_paths(self.graph, source=k[0], target=k[1]))
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
            print("Given transit function is NOT graphic as R", neq(), "I_{G_R}.")
            print("Violating transit sets:")
            for k in graphic_violating_sets:
                print(r(k[0], k[1]), " ", eq(), " ", sstr(self.transit_function[k]), " ", neq(), " ",
                      sstr(graphic_violating_sets[k]), " ", eq(), " I(",
                      str(k[0]).replace("'", ""), ",", str(k[1]).replace("'", ""), ")", sep="")
        print()

    def get_transit_function(self):
        return self.transit_function

    def get_axioms(self):
        return self.axioms

    def save_graph(self, csv_file):
        # Drawing graph figure and saving it
        nx.draw(self.graph, with_labels=True)
        plt.savefig(csv_file.split(".")[0] + ".png")
        print("\nG_R saved as", csv_file.split(".")[0] + ".png", "in working directory.\n")