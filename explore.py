import copy

import networkx as nx
from matplotlib import pyplot as plt
# from networkx.algorithms import isomorphism
import sys
from sys import argv
from math_strings import *
from graph_tools import *
import random
import stepfunction
import transit_function

def check_instance(ax_choice_true, ax_choice_false, check_object, vertices, signpost=False):

    if signpost:

        sf = stepfunction.stepfunction(stepfunction_set=check_object, vertices=vertices)

        ax_answer_true = sf.check_axioms(ax_choice_true, print_info=False)
        ax_answer_false = sf.check_axioms(ax_choice_false, print_info=False)

        # print("---")
        # print(check_object)
        # print("CHOICE SAT", ax_choice_sat)
        # print("CHOICE VIO", ax_choice_not_sat)
        # print("SAT?", ax_answer_true)
        # print("VIO?", ax_answer_false)
        # input()

        if False in ax_answer_true or True in ax_answer_false:
            return False
        else:
            return True

    else:

        tf = transit_function.transit_function(transit_function=check_object, vertices=vertices)

        ax_answer_true = tf.check_axioms(ax_choice_true, print_info=False)
        ax_answer_false = tf.check_axioms(ax_choice_false, print_info=False)

        # print("---")
        # print(check_object)
        # print("CHOICE SAT", ax_choice_sat)
        # print("CHOICE VIO", ax_choice_not_sat)
        # print("SAT?", ax_answer_true)
        # print("VIO?", ax_answer_false)

        if False in ax_answer_true or True in ax_answer_false:
            return False
        else:
            return True

def get_random_digraph(num_nodes, edge_probability):
    edges = []

    while len(edges) == 0:
        graph = nx.DiGraph()

        for i in range(0, num_nodes):
            graph.add_node(i)

        for u in range(num_nodes):
            for v in range(num_nodes):
                if u == v:
                    continue
                else:
                    thresh = random.random()
                    if thresh <= edge_probability:
                        graph.add_edge(u, v)

        edges = list(graph.edges())
    return graph

def get_random_graph(num_nodes, edge_probability):
    edges = []

    while len(edges) == 0:
        graph = nx.Graph()

        for i in range(0, num_nodes):
            graph.add_node(i)

        for u in range(num_nodes):
            for v in range(u + 1, num_nodes):
                if u == v:
                    continue
                else:
                    thresh = random.random()
                    if thresh <= edge_probability:
                        graph.add_edge(u, v)
        edges = list(graph.edges())

    return graph

axiom_strings_transit = [
            "t0", "t1", "t2s", "t2a", "t3",
            "tr2", "b1", "b2", "b3", "b4",
            "b6", "j2", "F", "G", "co0",
            "co1", "co2", "co3", "g", "p",
            "mod", "med", "b5", "rv", "ta", "graphic"
        ]

axiom_strings_stepfunctions = [
    "A", "B", "H", "C", "D", "F", "G", "E",
    "Pt", "Dd", "Dt", "Cw", "Cb", "Dm", "T1",
    "T2", "Tb2", "P4", "Sm", "graphic"
]

signpost = False
csv_file = ""
ax_choice_sat = []
ax_choice_not_sat = []
wrong_file_choice = False
no_file = True
random_graphs = False
num_nodes = 0
num_tries = 0
outdir = ""
write_output = False
random_function = False
probabilities = []

for arg in argv:

    # Print help string and exit if help argument was supplied
    if arg in ["-h", "--help", "--manual"]:
        print()
        # print("Call check.py with:")
        # print("python check.py -a [axioms] -f [filename]")
        # print("or")
        # print("python check.py --axioms [axioms] --file [filename]")
        # print("[axioms] should be axiom strings, comma separated, i.e. 'b1,b5,tr2'")
        # print("Please do not include any spaces in the axiom string.")
        # print("Stepsystems can be checked by including a -s argument, e.g. ")
        # print("python check.py -s -a [axioms] -f [filename]")
        # print()
        # print("Visualization of G_R/G_T will be saved under the same name as the input file with a .png extension.")
        # print()

        print("Supported Axioms (Transit Functions):")
        for a in axiom_strings_transit:
            print_axiom_info_tf(a)
            print()

        print()

        print("Supported Axioms (Step functions):")
        for a in axiom_strings_stepfunctions:
            print_axiom_info_sf(a)
            print()

        print()
        print("Select (transit function) axioms from:", sstr(axiom_strings_transit))
        print()
        print("Select (step function) axioms from:", sstr(axiom_strings_stepfunctions))
        print()
        sys.exit()

    if arg in ["--signpost"]:
        signpost = True

    if arg in ["--satisfies", "-s"]:
        try:
            ax_choice_sat = argv[argv.index(arg) + 1].split(",")
        except:
            wrong_ax_choice = True

    if arg in ["--probabilities", "-p"]:
        try:
            tmp_prob = argv[argv.index(arg) + 1].split(",")
            probabilities = [float(t) for t in tmp_prob]
        except:
            wrong_prob_choice = True
            print("Please check the -p [probabilities] parameter supplied. It should be a list of float values separated by ','.")
            print("I.e., 0.1,0.2,0.3,1.0")
            sys.exit()

    if arg in ["--violate", "-v"]:
        try:
            ax_choice_not_sat = argv[argv.index(arg) + 1].split(",")
        except:
            wrong_ax_choice = True

    if arg in ["--file", "-f"]:
        no_file = False
        try:
            csv_file = argv[argv.index(arg) + 1]
        except:
            wrong_file_choice = True

    if arg in ["-rg", "--randomgraph"]:
        random_graphs = True
        try:
            num_tries = int(argv[argv.index(arg) + 1])
        except:
            print("Please check the -rg [num_tries] parameter supplied. It should be an integer.")

    if arg in ["-rf", "--randomfunction"]:
        random_function = True
        try:
            num_tries = int(argv[argv.index(arg) + 1])
        except:
            print("Please check the -rf [num_tries] parameter supplied. It should be an integer.")

    if arg in ["-n", "--nodes"]:
        try:
            num_nodes = int(argv[argv.index(arg) + 1])
        except:
            print("Please check the -n [num_nodes] parameter supplied. It should be an integer.")

    if arg in ["-o", "--output"]:
        outdir = argv[argv.index(arg) + 1]
        if outdir[-1] != "/":
            outdir += "/"
        write_output = True

# Check if the axioms supplied are actually supported for signposts and exit otherwise
if signpost:
    not_supported_axioms = []
    for a in ax_choice_sat:
        if a not in axiom_strings_stepfunctions:
            not_supported_axioms += [a]

    for a in ax_choice_not_sat:
        if a not in axiom_strings_stepfunctions:
            not_supported_axioms += [a]

    if not_supported_axioms != []:
        print("Axioms", sstr(not_supported_axioms), "are not supported for Stepfunctions. ",
                                                    "Please alter your axiom string.")
        sys.exit()

# Check if the axioms supplied are actually supported for DTF and exit otherwise
if not signpost:
    not_supported_axioms = []
    for a in ax_choice_sat:
        if a not in axiom_strings_transit:
            not_supported_axioms += [a]

    for a in ax_choice_not_sat:
        if a not in axiom_strings_transit:
            not_supported_axioms += [a]

    if not_supported_axioms != []:
        print("Axioms", sstr(not_supported_axioms), "are not supported for Directed Transit Functions. ",
              "Please alter your axiom string.")
        sys.exit()

print(num_tries)

valid_graphs = 0

if not no_file:
    # TODO Randomly check adjacent transit functions with depth at most 2 for provided SP/TF.
    pass

else:
    if random_graphs:

        if signpost:

            counter = 0

            for edge_prob in probabilities:

                print()
                print("Checking edge probabiliy", edge_prob, "...")
                print("--------------------------------")

                for i in range(num_tries):

                    if counter % 100 == 0:
                        print()
                        print(counter, "graphs checked ...")

                    counter += 1

                    graph = get_random_graph(num_nodes, edge_prob)
                    vertices = list(graph.nodes())

                    stepfunction_set = graph_to_step(graph)

                    fits_axioms = check_instance(ax_choice_sat, ax_choice_not_sat, stepfunction_set, vertices, signpost)

                    # print("Fits?", fits_axioms)

                    if fits_axioms:
                        print()
                        print("Nodes:", sstr(vertices))
                        print("Edges:", sstr(list(graph.edges())))
                        print("Stepfunction:", sstr(stepfunction_set))
                        if write_output:
                            save_graph(graph, outdir + "example_" + str(valid_graphs) + ".png")
                        valid_graphs += 1

        else:
            counter = 0

            for edge_prob in probabilities:
                print()
                print("Checking edge probabiliy", edge_prob, "...")
                print("--------------------------------")
                print()
                for i in range(num_tries):

                    if counter % 100 == 0:
                        print()
                        print(counter, "graphs checked ...")

                    counter += 1

                    graph = get_random_digraph(num_nodes, edge_prob)
                    vertices = list(graph.nodes())

                    transit_function_test = graph_to_transit(graph)

                    fits_axioms = check_instance(ax_choice_sat, ax_choice_not_sat, transit_function_test, vertices, signpost)

                    # print(sstr(list(graph.edges())))
                    # print(vertices)
                    # print(edge_prob)
                    # print("FITS", fits_axioms)
                    # input()


                    if fits_axioms:
                        print()
                        print("Nodes:", sstr(vertices))
                        print("Edges:", sstr(list(graph.edges())))
                        print("Transit Function:", transit_function_test)
                        if write_output:
                            save_graph(graph, outdir + "example_" + str(valid_graphs) + ".png")
                        valid_graphs += 1

    elif random_function:
        valid_graphs = 0
        if signpost:

            triple_list = set()

            vertices = [i for i in range(num_nodes)]

            for u in vertices:
                for v in vertices:
                    for w in vertices:
                        if u == w or u == v:
                            continue
                        triple_list.update({(u, v, w)})

            counter = 0

            for tprob in probabilities:

                print()
                print("Checking tuple probabiliy", tprob, "...")
                print("--------------------------------")
                print()

                for i in range(num_tries):

                    if counter % 100 == 0:
                        print()
                        print(counter, "graphs checked ...")

                    counter += 1

                    triple_selection = []

                    for t in triple_list:
                        thresh = random.random()

                        if thresh <= tprob:
                            triple_selection += [t]

                    stepfunction_set = triple_selection

                    # input(stepfunction_set)

                    fits_axioms = check_instance(ax_choice_sat, ax_choice_not_sat, stepfunction_set, vertices, signpost)

                    if fits_axioms:
                        graph = step_to_graph(stepfunction_set)

                        print()
                        print("Nodes:", sstr(vertices))
                        print("Edges:", sstr(list(graph.edges())))
                        print("Stepfunction:", sstr(stepfunction_set))
                        if write_output:
                            save_graph(graph, outdir + "example_" + str(valid_graphs) + ".png")
                            save_step_function(stepfunction_set, outdir + "example_" + str(valid_graphs) + ".tsv", vertices)
                        valid_graphs += 1
        else:
            vertices = [i for i in range(num_nodes)]

            counter = 0

            transit_function_dict = dict()

            for u in vertices:
                for v in vertices:
                    if u == v:
                        transit_function_dict[(u, v)] = {u}
                    else:
                        transit_function_dict[(u, v)] = set()

            for tprob in probabilities:

                print()
                print("Checking transit set probability", tprob, "...")
                print("--------------------------------")
                print()

                for i in range(num_tries):

                    if counter % 100 == 0:
                        print()
                        print(counter, "graphs checked ...")

                    counter += 1

                    transit_function_dict_copy = copy.copy(transit_function_dict)

                    for u in vertices:
                        for v in vertices:
                            if u == v:
                                continue

                            vertex_selection = []

                            added = False

                            for w in vertices:
                                thresh = random.random()
                                if thresh <= tprob:
                                    added = True
                                    vertex_selection += [w]

                            transit_function_dict_copy[(u, v)] = transit_function_dict_copy[(u, v)].union(vertex_selection)

                            if u not in transit_function_dict_copy[(u, v)] and added:
                                transit_function_dict_copy[(u, v)] = transit_function_dict_copy[(u, v)].union([u])
                            if v not in transit_function_dict_copy[(u, v)] and added:
                                transit_function_dict_copy[(u, v)] = transit_function_dict_copy[(u, v)].union([v])

                    fits_axioms = check_instance(ax_choice_sat, ax_choice_not_sat, transit_function_dict_copy, vertices,
                                                 signpost)

                    # print(sstr(list(graph.edges())))
                    # print(vertices)
                    # print(edge_prob)
                    # print("FITS", fits_axioms)
                    # input()

                    if fits_axioms:
                        graph = transit_to_graph(transit_function_dict_copy)
                        print()
                        print("Nodes:", sstr(vertices))
                        print("Edges:", sstr(list(graph.edges())))
                        print("Transit Function:", transit_function_dict_copy)
                        if write_output:
                            save_graph(graph, outdir + "example_" + str(valid_graphs) + ".png")
                            save_transit_function(transit_function_dict_copy, outdir + "example_" + str(valid_graphs) + ".tsv", vertices)
                        valid_graphs += 1




    else:
        graph_atlas = nx.graph_atlas_g()
        valid_graphs = 0

        if signpost:

            counter = 0

            for graph in graph_atlas:

                if counter % 100 == 0:
                    print()
                    print(counter, "graphs checked ...")

                counter += 1

                vertices = list(graph.nodes())

                stepfunction_set = graph_to_step(graph)

                fits_axioms = check_instance(ax_choice_sat, ax_choice_not_sat, stepfunction_set, vertices, signpost)

                if fits_axioms:
                    print()
                    print("Nodes:", sstr(vertices))
                    print("Edges:", sstr(list(graph.edges())))
                    print("Stepfunction:", sstr(stepfunction_set))
                    if write_output:
                        save_graph(graph, outdir + "example_" + str(valid_graphs) + ".png")
                    valid_graphs += 1

        elif not signpost:

            counter = 0

            for graph in graph_atlas:

                if counter % 100 == 0:
                    print()
                    print(counter, "graphs checked ...")

                counter += 1

                vertices = list(graph.nodes())

                transit_function_test = graph_to_transit(graph)

                fits_axioms = check_instance(ax_choice_sat, ax_choice_not_sat, transit_function_test, vertices,
                                             signpost)

                if fits_axioms:
                    print()
                    print("Nodes:", sstr(vertices))
                    print("Edges:", sstr(list(graph.edges())))
                    print("Transit Function:", transit_function_test)
                    if write_output:
                        save_graph(graph, outdir + "example_" + str(valid_graphs) + ".png")
                    valid_graphs += 1



if signpost and no_file:
    print(valid_graphs, "explored step systems satisfied the constraints")
elif not signpost and no_file:
    print(valid_graphs, "explored transit functions satisfied the constraints")
