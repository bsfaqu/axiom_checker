import networkx as nx
import copy
from math_strings import *
from sf_axioms import axioms
from matplotlib import pyplot as plt
from graph_tools import *

class stepfunction:

    stepfunction_set = set()
    stepfunction_dict = {}
    graph = None
    vertices = None
    axioms = None

    def __init__(self, csv_lines):
        # Parse vertices from the first line
        vertices = csv_lines[0].split("\t")[1::]

        # Remove the first line (only contains vertices)
        csv_lines = csv_lines[1::]

        # Here we save all the transit sets. Keys are tuples (u,v) and values are sets.
        stepfunction_dict = {}

        # Transit sets that are always supposed to be empty, i.e fields filled
        # with "", hence no string
        ignore_tuples = []

        # Initialize transit sets as empty and ensure (t3)
        for u in vertices:
            for v in vertices:
                stepfunction_dict[(u, v)] = set()

                # # Enforce (t3)
                # if u == v:
                #     stepfunction_dict[(u, v)] = {u}

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

                # ignore line, hence this step set is kept empty
                elif line[i] == "":
                    target = vertices[i]

                    # Keep track of purposefully emptpy sets
                    ignore_tuples += [(source, target)]
                else:
                    # Set transit sets in transit_function. R(u,u) entries are ignored.
                    target = vertices[i]
                    # if source == target:
                    #     continue
                    # else:
                    transit_list = line[i].split(",")
                    stepfunction_dict[(source, target)] = set(transit_list)

        stepfunction_set = self.step_dic_to_set(stepfunction_dict)

        # Output supplied stepfunction
        print("\n---\n")
        print("*** Stepfunction before step-adding ***")

        counter = 0

        for t in stepfunction_set:
            print(tstr(t))

        # Save the original transit function
        orig_stepfunction_dict = copy.copy(stepfunction_dict)

        # Initialize NetworkX graph object to obtain shortest paths later
        graph = nx.Graph()

        # Add all the vertices
        for vert in vertices:
            graph.add_node(vert)

        # Add edges to graph if tuple is (u, v, v).
        for t in stepfunction_set:
            if t[1] == t[2]:
                graph.add_edge(t[0], t[1])

        # Output edges of G_R
        print("\n---\n")
        print("*** Constructed edges ***")
        print(sstr(list(graph.edges())).replace("'", ""))

        # Keep track of added paths
        added_paths = []

        for k in stepfunction_dict:
            # If the step triple is supposed to be empty
            if k in ignore_tuples or k[0] == k[1]:
                continue

            # Get all the shortest paths with nx
            try:
                paths = list(nx.all_shortest_paths(graph, source=k[0], target=k[1]))
            except nx.NetworkXNoPath:
                continue

            # Is there only one path
            if len(paths) == 1:
                # Does the path only contain one vertex (u = v), continue.
                if len(paths[0]) == 1:
                    continue
                # # Does the path contain two vertices (edge must be defined as such already), continue
                # if len(paths[0]) == 2:
                #     continue

            # If the transit set for this tuple is not set yet (not supplied by user)
            if stepfunction_dict[k] == set():
                t_set = set()

                # Collecting all the first vertices along all shortest paths in t_set
                for p in paths:
                    t_set = t_set.union({p[1]})
                    added_paths += [k]

                # Set the transit set of current tuple to t_set
                stepfunction_dict[k] = t_set
            else:
                pass

        # output the added paths
        for t in added_paths:
            print("Added path(s) for", str(t[0]).replace("'", ""), rarrow(), t[1].replace("'", ""))

        if len(added_paths) > 0:
            print()

        # Output the transit function after adding the shortest paths in G_R
        print("\n---\n")
        print("*** Step Function after step-adding (as transit function) ***")

        # Provide a structured output of the transit function
        counter = 0
        for k in stepfunction_dict:
            if counter % len(vertices) == 0 and counter != 0:
                print("-")
            print(r(k[0], k[1]), eq(), sstr(stepfunction_dict[k]))
            counter += 1

        print("\n---\n")
        print("*** Step Function after step-adding (as set) ***")

        stepfunction_set = self.step_dic_to_set(stepfunction_dict)
        for t in stepfunction_set:
            print(tstr(t))

        # Store stetpfunction dict in class variable
        self.stepfunction_dict = stepfunction_dict

        # Store stepfunction set in class variable
        self.stepfunction_set = stepfunction_set

        # Initialize axioms with transit function and save in class variable
        self.axioms = axioms(self.stepfunction_set)

        # Save digraph to class variable
        self.graph = graph

        self.vertices = vertices

    def step_dic_to_set(self, stepfunction_dic, print_info=True):
        stepfunction_set = []

        for k in stepfunction_dic.keys():
            for s in stepfunction_dic[k]:
                stepfunction_set += [(k[0], s, k[1])]

        return set(stepfunction_set)

    def check_axioms(self, ax_choice):

        sat_list = [False for a in ax_choice]

        if "A" in ax_choice:
            print("Check (A)...\n")
            for u in self.vertices:
                for v in self.vertices:
                    for x in self.vertices:
                        self.axioms.A(u, v, x)

        if "B" in ax_choice:
            print("Check (B)...\n")
            for u in self.vertices:
                for v in self.vertices:
                    for x in self.vertices:
                        self.axioms.B(u, v, x)

        if "H" in ax_choice:
            print("Check (H)...\n")
            for u in self.vertices:
                for v in self.vertices:
                    self.axioms.H(u, v)

        if "C" in ax_choice:
            print("Check (C)...\n")
            for u in self.vertices:
                for v in self.vertices:
                    for x in self.vertices:
                        for y in self.vertices:
                            self.axioms.C(u, v, x, y)

        if "D" in ax_choice:
            print("Check (D)...\n")
            for u in self.vertices:
                for v in self.vertices:
                    for x in self.vertices:
                        for y in self.vertices:
                            self.axioms.D(u, v, x, y)

        if "F" in ax_choice:
            print("Check (F)...\n")
            for u in self.vertices:
                for v in self.vertices:
                    for x in self.vertices:
                        for y in self.vertices:
                            self.axioms.F(u, v, x, y)

        if "G" in ax_choice:
            print("Check (G)...\n")
            for u in self.vertices:
                for v in self.vertices:
                    for x in self.vertices:
                        for y in self.vertices:
                            self.axioms.G(u, v, x, y)

        if "E" in ax_choice:
            print("Check (E)...\n")
            for u in self.vertices:
                for v in self.vertices:
                    for x in self.vertices:
                        for y in self.vertices:
                            self.axioms.E(u, v, x, y)

        if "Pt" in ax_choice:
            print("Check (Pt)...\n")
            for u in self.vertices:
                for v in self.vertices:
                    for x in self.vertices:
                        for y in self.vertices:
                            self.axioms.Pt(u, v, x, y)

        if "Dd" in ax_choice:
            print("Check (Dd)...\n")
            for u in self.vertices:
                for v in self.vertices:
                    for w in self.vertices:
                        for x in self.vertices:
                            for y in self.vertices:
                                for z in self.vertices:
                                    for d in self.vertices:
                                        self.axioms.Dd(u, v, w, x, y, z, d)

        if "Dt" in ax_choice:
            print("Check (Dt)...\n")
            for u in self.vertices:
                for v in self.vertices:
                    for x in self.vertices:
                        for y in self.vertices:
                            for z in self.vertices:
                                self.axioms.Dt(u, v, x, y, z)

        if "Cw" in ax_choice:
            print("Check (Cw)...\n")
            for u in self.vertices:
                for v in self.vertices:
                    for x in self.vertices:
                        for y in self.vertices:
                            self.axioms.Cw(u, v, x, y)

        if "Cb" in ax_choice:
            print("Check (Cb)...\n")
            for u in self.vertices:
                for v in self.vertices:
                    for w in self.vertices:
                        for x in self.vertices:
                            for y in self.vertices:
                                self.axioms.Cb(u, v, w, x, y)

        if "Dm" in ax_choice:
            print("Check (Dm)...\n")
            for u in self.vertices:
                for v in self.vertices:
                    for x in self.vertices:
                        for y in self.vertices:
                            self.axioms.Dm(u, v, x, y)

        if "T1" in ax_choice:
            print("Check (T1)...\n")
            for x in self.vertices:
                for y in self.vertices:
                    for t in self.vertices:
                        self.axioms.T1(x, y, t)

        if "T2" in ax_choice:
            print("Check (T2)...\n")
            for x in self.vertices:
                for y in self.vertices:
                    for z in self.vertices:
                        self.axioms.T2(x, y, z)

        if "Tb2" in ax_choice:
            print("Check (Tb2)...\n")
            for x in self.vertices:
                for y in self.vertices:
                    for z in self.vertices:
                        self.axioms.Tb2(x, y, z, self.vertices)

        if "P4" in ax_choice:
            print("Check (P4)...\n")
            for u in self.vertices:
                for v in self.vertices:
                    for x in self.vertices:
                        for y in self.vertices:
                            self.axioms.P4(u, v, x, y)

        if "Sm" in ax_choice:
            print("Check (Sm)...\n")
            for u in self.vertices:
                for v in self.vertices:
                    for w in self.vertices:
                        for x in self.vertices:
                            for y in self.vertices:
                                for z in self.vertices:
                                    self.axioms.Sm(u, v, w, x, y, z)


    def check_additional(self):
        test_stepfunction = graph_to_step(self.graph)

        t_in_graph_not_in_sf = []
        t_in_sf_not_in_graph = []

        for t in test_stepfunction:
            if t not in self.stepfunction_set:
                t_in_graph_not_in_sf += [t]

        for t in self.stepfunction_set:
            if t not in test_stepfunction:
                t_in_sf_not_in_graph += [t]

        if len(t_in_graph_not_in_sf) == 0 and len(t_in_sf_not_in_graph) == 0:
            print("The step system of G_T is equal to the step function provided.")
        else:
            print("The step system of G_T differs from the step function provided.")

            print()
            print("Triples derived from G_T that are not in T:")

            for t in t_in_graph_not_in_sf:
                print(t)

            print()
            print("Triples in T that cannot be derived from G_T:")

            for t in t_in_sf_not_in_graph:
                print(t)


    def save_graph(self, csv_file):
        # Drawing graph figure and saving it
        nx.draw(self.graph, with_labels=True)
        plt.savefig(csv_file.split(".")[0] + ".png")
        print("\nG_R saved as", csv_file.split(".")[0] + ".png", "in working directory.\n")