import copy

import networkx as nx
from matplotlib import pyplot as plt
from networkx.algorithms import isomorphism
import sys
from sys import argv
from math_strings import *
from graph_tools import *
import random
import stepfunction
import transit_function
import itertools as it
import os

def check_instance(ax_choice_true, ax_choice_false, check_object, vertices, signpost=False):

    # Signpost or no signpost flag
    if signpost:

        # Create stepfunction from stepfunction set
        sf = stepfunction.stepfunction(stepfunction_set=check_object, vertices=vertices)

        # Check if sat axioms dont matter
        if ax_choice_true == ["X"]:
            ax_answer_true = [True]
        # Else we check the results for every axiom thats supposed to be sat
        else:
            ax_answer_true = sf.check_axioms(ax_choice_true, print_info=False)

        # Check if sat axioms dont matter
        if ax_choice_false == ["X"]:
            ax_answer_false = [False]
        # Else we check the results for every axiom thats supposed to be not sat
        else:
            ax_answer_false = sf.check_axioms(ax_choice_false, print_info=False)

        # Check if instance satisfies constraints, i.e. if all pos axioms are satisfied and all neg
        # axioms are not satisfied
        if False in ax_answer_true or True in ax_answer_false:
            return False
        else:
            return True

    else:

        # Create transit function from transit function dic
        tf = transit_function.transit_function(transit_function=check_object, vertices=vertices)

        # Check if sat axioms dont matter
        if ax_choice_true == ["X"]:
            ax_answer_true = [True]
        # Else we check the results for every axiom thats supposed to be sat
        else:
            ax_answer_true = tf.check_axioms(ax_choice_true, print_info=False)

        # Check if not sat axioms dont matter
        if ax_choice_false == ["X"]:
            ax_answer_false = [False]
        # Else we check the results for every axiom thats supposed to be not sat
        else:
            ax_answer_false = tf.check_axioms(ax_choice_false, print_info=False)

        # Check if instance satisfies constraints, i.e. if all pos axioms are satisfied and all neg
        # axioms are not satisfied
        if False in ax_answer_true or True in ax_answer_false:
            return False
        else:
            return True

def get_random_digraph(num_nodes, edge_probability):
    edges = []

    # randomly add edges to graph until there is at least one edge
    while len(edges) == 0:

        # Init directed graph
        graph = nx.DiGraph()

        # Add the vertices
        for i in range(0, num_nodes):
            graph.add_node(i)

        # For each pair of vertices, randomly determine with edge_probabilty
        # If they are connected with an edge
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

    # randomly add edges to graph until there is at least one edge
    while len(edges) == 0:
        # Init graph
        graph = nx.Graph()

        # Add the vertices
        for i in range(0, num_nodes):
            graph.add_node(i)

        # For each pair of vertices, randomly determine with edge_probabilty
        # If they are connected with an edge
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

def is_distance_hereditary(graph):
    nodes = graph.nodes()

    for u in nodes:
        for v in nodes:
            for w in nodes:
                for x in nodes:
                    try:
                        d_uv = nx.shortest_path_length(graph, u, v)
                    except:
                        continue
                        d_uv = -1
                    try:
                        d_wx = nx.shortest_path_length(graph, w, x)
                    except:
                        continue
                        d_wx = -1
                    try:
                        d_uw = nx.shortest_path_length(graph, u, w)
                    except:
                        continue
                        d_uw = -1
                    try:
                        d_vx = nx.shortest_path_length(graph, v, x)
                    except:
                        continue
                        d_vx = -1
                    try:
                        continue
                        d_ux = nx.shortest_path_length(graph, u, x)
                    except:
                        continue
                        d_ux = -1
                    try:
                        continue
                        d_vw = nx.shortest_path_length(graph, v, w)
                    except:
                        continue
                        d_vw = -1

                    distance_set = {d_uv + d_wx, d_uw + d_vx, d_ux + d_vw}

                    if len(distance_set) > 2:
                        return False
    return True


# Allowed transit function axioms
axiom_strings_transit = [
            "t0", "t1", "t2s", "t2a", "t3",
            "tr2", "b1", "b2", "b3", "b4",
            "b6", "j2", "F", "G", "co0",
            "co1", "co2", "co3", "g", "p",
            "mod", "med", "b5", "rv", "ta", "graphic"
        ]

# Allowed stepsytem axioms
axiom_strings_stepfunctions = [
    "A", "B", "H", "C", "D", "F", "G", "E",
    "Pt", "Dd", "Dt", "Cw", "Cb", "Dm", "T1",
    "T2", "Tb2", "P4", "Sm", "graphic", "X"
]

# Some flags for CLI input.
# Signpost system or not
signpost = False

# Csv that contains a stepsystem/tf
csv_file = ""

# Axioms supplied
ax_choice_sat = []
ax_choice_not_sat = []

wrong_file_choice = False
no_file = True

# Random graph mode?
random_graphs = False
num_nodes = 0
num_tries = 0

# Write output?
outdir = ""
write_output = False

# Random Function Mode?
random_function = False

# Probabilities for random function or random_graph mode
probabilities = []

# Flags for connectedness filters
connected = False
two_connected = False

# Forbidden subgraph flags
check_free_of = False
forbidden_subgraphs = []
subgraph_dir = ""

# Contains induced subgraph flags
check_contains = False
induced_subgraphs = []
induced_subgraph_dir = ""

distance_hereditary = False
distance_regular = False


for arg in argv:

    # Print help string and exit if help argument was supplied
    if arg in ["-h", "--help", "--manual"]:
        print()
        print("explore.py is a python command line utility to generate examples of directed transit functions and "
              "signpost systems that satisfy a given set of axioms, and violate another set of given axioms.")
        print()
        print("explore.py supports multiple modes. Please include the --signpost if you want to check "
              "signpost systems.")
        print()
        print("For every mode, the -s/--satisfies [axioms] or -v/--violates [axioms] flags have to be included.")
        print("For every mode, explore ensures that the generated exampels satisfy the -s [axioms] and violate the"
              " -v [axioms].")
        print()
        print("-s/--satisfies and -v/--violates have to be followed with a comma separated axiom string, e.g. 'b1,b5,tr2'.")
        print()
        print("In case no axioms are required to be satisfied/violated, just an 'X' can be supplied, e.g. -s X or -v X.")
        print()
        print("Take note that 'graphic' can also be included as an axiom, for which is then checked if R_{G_R} = R "
              "for directed transit functions, and the analogue for signpost systems.")
        print()
        print()
        print("Iterate all undirected graphs <= 7 vertices:")
        print("--------------------------------------------")
        print()
        print("This can be done with:")
        print("python explore.py [--signpost] --satisfies [axioms] --violates [axioms].")
        print("OR")
        print("python explore.py [--signpost] -s [axioms] -v [axioms].")
        print()
        print("The --signpost flag is optional, hence should be used if you want to explore signpost systems.")
        print()
        print("Optional arguments include:")
        print("-n [integer] / --nodes [integer] - For a minimum number of vertices.")
        print("-o [directory] / --output [directory] - To write .png/.tsv of the generated examples to the directory.")
        print("--connected - To filter for connected graphs")
        print("--2connected - To filter for two-connected graphs")
        print("--contains [directory] - To filter for graphs containing induced subgraphs.")
        print("                         There should be .tsv files with transit functions/signpost systems that")
        print("                         contain these induced subgraphs. File format should be the same as required for")
        print("                         check.py. Can also be the output directory from another explore.py call.")
        print("--free [directory]     - To filter for graphs NOT containing induced subgraphs.")
        print("                         There should be .tsv files with transit functions/signpost systems that")
        print("                         describe these forbidden subgraphs. File format should be the same as required for")
        print("                         check.py. Can also be the output directory from another explore.py call.")

        print()
        print()
        print("Generate random graphs (undirected for --signpost, directed for DTF)")
        print("--------------------------------------------")
        print()
        print("This can be done with:")
        print("python explore.py [--signpost] --satisfies [axioms] --violates [axioms] --randomgraph [num_tries] "
              "--nodes [num_nodes] --probabilities [probabilitylist].")
        print("OR")
        print("python explore.py [--signpost] -s [axioms] -v [axioms] -rg [num_tries] -n [num_nodes] -p [probabilitylist].")
        print()
        print("The [probabilitylist] should be a comma-separated list of edge-probabilities. Make sure to not include any"
              " spaces in this string. For example, '-p 0.1,0.2,0.3,0.9' is a valid probability string. ")
        print()
        print("The --signpost flag is optional, hence should be used if you want to explore signpost systems.")
        print()
        print("For example")
        print("explore.py -s [sat_axioms] -v [viol_axioms] -rg 100 -n 5 -p 0.1,0.3,0.7 -o examples/")
        print()
        print("Randomly generates 100 graphs of 5 vertices with edge probability 10%, ...,  100 graphs of 5 vertices "
              "with edge probability 70% and checks for each of them if they satisfy the axioms [sat_axioms] and violate"
              " the [viol_axioms]. Graphs that satisfy [sat_axioms] and violate [viol_axioms] are saved to the examples/"
              " directory in .tsv format (and their visualization as .png).")
        print()
        print("Optional arguments include:")
        print("-o [directory] / --output [directory] - To write .png (figure) and .tsv of the generated examples to "
              "the directory.")
        print("--connected - To filter for connected graphs")
        print("--2connected - To filter for two-connected graphs")
        print("--contains [directory] - To filter for graphs containing induced subgraphs.")
        print("                         There should be .tsv files with transit functions/signpost systems that")
        print("                         contain these induced subgraphs. File format should be the same as required for")
        print("                         check.py. Can also be the output directory from another explore.py call.")
        print("--free [directory]     - To filter for graphs NOT containing induced subgraphs.")
        print("                         There should be .tsv files with transit functions/signpost systems that")
        print("                         describe these forbidden subgraphs. File format should be the same as required for")
        print("                         check.py. Can also be the output directory from another explore.py call.")

        print()
        print()
        print("Generate random functions")
        print("--------------------------------------------")
        print()
        print("This can be done with:")
        print("python explore.py [--signpost] --satisfies [axioms] --violates [axioms] --randomfunction [num_tries] "
              "--nodes [num_nodes] --probabilities [probabilitylist].")
        print("OR")
        print(
            "python explore.py [--signpost] -s [axioms] -v [axioms] -rf [num_tries] -n [num_nodes] -p [probabilitylist].")
        print()
        print(
            "The [probabilitylist] should be a comma-separated list of edge-probabilities. Make sure to not include any "
            "spaces in this string. For example, '-p 0.1,0.2,0.3,0.9' is a valid probability string. ")
        print()
        print("The --signpost flag is optional, hence should be used if you want to explore signpost systems.")
        print()
        print("For example,")
        print("explore.py -s [sat_axioms] -v [viol_axioms] -rf 100 -n 5 -p 0.1,0.3,0.7 -o examples/")
        print()
        print("Randomly generates 100 directed transit functions on 5 vertices with the 'inclusion-probability 10%',"
              " ..., 100 directed transit functions on 5 vertices with the 'inclusion-probability 70%'. Inclusion"
              " probability here conceptually is that for every R(u,v), all remaining vertices are included in R(u,v)"
              " with P(x in R(u,v))=0.1/0.3/0.7. The method for randomly creating these always ensures that u,v in R(u,v)"
              " if R(u,v) is not empty. Similarly it ensures that u in R(u, u).")
        print()
        print("For signpost systems, the set of all possiple triples on [num_vertices] is computed and then 10%/.../70%"
              " of these tuples are randomly selected and the signpost system is checked for the axioms.")
        print()
        print("Optional arguments include:")
        print("-o [directory] / --output [directory] - To write .png (figure) and .tsv of the generated examples to "
              "the directory.")
        print()
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
        print("--------------------------------------------")
        for a in axiom_strings_transit:
            print_axiom_info_tf(a)
            print()

        print()

        print("Supported Axioms (Step functions):")
        print("--------------------------------------------")
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

    if arg in ["--connected"]:
        connected = True

    if arg in ["--2connected"]:
        two_connected = True

    if arg in ["--distancehereditary"]:
        distance_hereditary = True

    if arg in ["--distanceregular"]:
        distance_regular = True

    if arg in ["--free"]:
        check_free_of = True
        try:
            subgraph_dir = argv[argv.index(arg) + 1]
            if subgraph_dir[-1] != "/":
                subgraph_dir += "/"
        except:
            print("Please check the argument provided for the subgraph directory.")

    if arg in ["--contains"]:
        check_free_of = True
        try:
            induced_subgraph_dir = argv[argv.index(arg) + 1]
            if induced_subgraph_dir[-1] != "/":
                induced_subgraph_dir += "/"
        except:
            print("Please check the argument provided for the subgraph directory.")


# Check input for signpost systems
if signpost:

    # Check if the axioms selected are supported
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

    # Read and save all forbidden subgraphs from the directory supplied
    if check_free_of:
        filenames = []
        for path, subdirs, files in os.walk(subgraph_dir):
            for name in files:
                if ".tsv" in name:
                    filenames += [os.path.join(path, name)]

        for fpath in filenames:
            with open(fpath, "r") as f:
                csv_lines = f.read()
                csv_lines = csv_lines.split("\n")

            sf = stepfunction.stepfunction(csv_lines)
            forbidden_subgraphs += [sf.get_graph()]

    # Read and save all induced subgraphs from the directory supplied
    if check_contains:
        filenames = []
        for path, subdirs, files in os.walk(subgraph_dir):
            for name in files:
                if ".tsv" in name:
                    filenames += [os.path.join(path, name)]

        for fpath in filenames:
            with open(fpath, "r") as f:
                csv_lines = f.read()
                csv_lines = csv_lines.split("\n")

            sf = stepfunction.stepfunction(csv_lines)
            induced_subgraphs += [sf.get_graph()]


# Check input for (directed) transit functions
if not signpost:

    # Check if the axioms selected are supported
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

    # Read and save all forbidden subgraphs from the directory supplied
    if check_free_of:
        filenames = []
        for path, subdirs, files in os.walk(subgraph_dir):
            for name in files:
                if ".tsv" in name:
                    filenames += [os.path.join(path, name)]

        for fpath in subgraph_dir:
            with open(fpath, "r") as f:
                csv_lines = f.read()
                csv_lines = csv_lines.split("\n")

            tf = transit_function.transit_function(csv_lines=csv_lines)
            forbidden_subgraphs += [tf.get_graph()]

    # Read and save all induced subgraphs from the directory supplied
    if check_contains:
        filenames = []
        for path, subdirs, files in os.walk(subgraph_dir):
            for name in files:
                if ".tsv" in name:
                    filenames += [os.path.join(path, name)]

        for fpath in filenames:
            with open(fpath, "r") as f:
                csv_lines = f.read()
                csv_lines = csv_lines.split("\n")

            tf = transit_function.transit_function(csv_lines=csv_lines)
            induced_subgraphs += [tf.get_graph()]


valid_graphs = 0

# If adjacency mode is selected, i.e. an input file is supplied
if not no_file:

    if signpost:

        try:
            # Read input file
            with open(csv_file, "r") as f:
                csv_str = f.read()

            # Get the lines
            csv_lines = csv_str.split("\n")

            # Parse vertices from the first line
            vertices = csv_lines[0].split("\t")[1::]
        except Exception as e:
            print()
            print("Something went wrong reading the .tsv file. Reading the file and parsing the vertices "
                  "produced the following exception:")
            raise

        stepfunction_obj = stepfunction.stepfunction(csv_lines)
        stepfunction_set = stepfunction_obj.get_stepfunction()

        stepfunction_delete_set = copy.copy(stepfunction_set)
        stepfunction_delete_set.update({"*"})

        triple_list = set()

        vertices = stepfunction_obj.get_vertices()

        for u in vertices:
            for v in vertices:
                for w in vertices:
                    if u == w or u == v:
                        continue
                    triple_list.update({(u, v, w)})

        triple_list.update({"*"})

        for s in stepfunction_set:
            triple_list.remove(s)

        alterations = it.product(triple_list, triple_list, stepfunction_delete_set, stepfunction_delete_set)

        print()
        print("Altering the provided step function ... ")

        for a in alterations:
            stepfunction_test = copy.copy(stepfunction_set)

            t_add_0 = a[0]
            t_add_1 = a[1]
            t_delete_0 = a[2]
            t_delete_1 = a[3]

            if t_add_0 == t_add_1 and t_add_0 != "*":
                continue

            if t_delete_0 == t_delete_1 and t_delete_0 != "*":
                continue

            if t_add_0 in [t_delete_0, t_delete_1] and t_add_0 != "*":
                continue

            if t_add_1 in [t_delete_0, t_delete_1] and t_add_1 != "*":
                continue

            if t_add_0 != "*":
                stepfunction_test.update({t_add_0})

            if t_add_1 != "*":
                stepfunction_test.update({t_add_1})

            if t_delete_0 != "*":
                try:
                    stepfunction_test.remove(t_delete_0)
                except:
                    pass

            if t_delete_0 != "*":
                try:
                    stepfunction_test.remove(t_delete_0)
                except:
                    pass

            # print()
            # print("ADD", t_add_0)
            # print("ADD", t_add_1)
            # print("DELETE", t_delete_0)
            # print("DELETE", t_delete_1)
            # print("ORIGINAL STEPSYSTEM", stepfunction_set)
            # print("ALTERED STEPSYSTEM ", stepfunction_test)

            fits_axioms = check_instance(ax_choice_sat, ax_choice_not_sat, stepfunction_test, vertices, signpost)

            if fits_axioms:
                print()
                graph = step_to_graph(stepfunction_test)
                print("Nodes:", sstr(vertices))
                print("Edges:", sstr(list(graph.edges())))
                print("Stepfunction:", sstr(stepfunction_test))
                if write_output:
                    save_graph(graph, outdir + "example_" + str(valid_graphs) + ".png")
                    save_step_function(stepfunction_test)
                valid_graphs += 1

    else:
        # TODO implement the adjacency checking for the transit function
        pass

# Random graph mode
elif random_graphs:
    print("Checking Random Graphs with", num_nodes, "vertices.")
    print("-----------------------------------")

    if signpost:

        counter = 0
        pass_filter = 0

        for edge_prob in probabilities:

            print()
            print("Checking edge probabiliy", edge_prob, "...")
            print("--------------------------------")

            for i in range(num_tries):

                if counter % 100 == 0:
                    print()
                    print(counter, "graphs checked ...", pass_filter, "passed filtering.")

                counter += 1

                graph = get_random_graph(num_nodes, edge_prob)

                if connected:
                    if nx.is_connected(graph):
                        pass
                    else:
                        continue

                if two_connected:
                    if nx.is_biconnected(graph):
                        pass
                    else:
                        continue

                if distance_hereditary:
                    if is_distance_hereditary(graph):
                        pass
                    else:
                        continue

                if distance_regular:
                    if nx.is_distance_regular(graph):
                        pass
                    else:
                        continue

                if check_free_of:
                    is_free_of = True
                    for sg in forbidden_subgraphs:
                        GM = isomorphism.GraphMatcher(graph, sg)
                        res = GM.subgraph_is_isomorphic()
                        if res:
                            is_free_of = False
                    if not is_free_of:
                        continue

                if check_contains:
                    contains = False
                    for sg in forbidden_subgraphs:
                        GM = isomorphism.GraphMatcher(graph, sg)
                        res = GM.subgraph_is_isomorphic()
                        if res:
                            is_free_of = True
                    if contains:
                        pass
                    else:
                        continue

                pass_filter += 1

                vertices = list(graph.nodes())

                stepfunction_set = graph_to_step(graph)

                fits_axioms = check_instance(ax_choice_sat, ax_choice_not_sat, stepfunction_set, vertices, signpost)


                if fits_axioms:
                    print()
                    print("Nodes:", sstr(vertices))
                    print("Edges:", sstr(list(graph.edges())))
                    print("Stepfunction:", sstr(stepfunction_set))
                    if write_output:
                        save_step_function(stepfunction_set, outdir + "example_" + str(valid_graphs) + ".tsv", vertices)
                        save_graph(graph, outdir + "example_" + str(valid_graphs) + ".png")
                    valid_graphs += 1

    else:

        counter = 0
        pass_filter = 0

        for edge_prob in probabilities:
            print()
            print("Checking edge probabiliy", edge_prob, "...")
            print("--------------------------------")
            print()
            for i in range(num_tries):

                if counter % 100 == 0:
                    print()
                    print(counter, "graphs checked ...", pass_filter, "passed filtering.")

                counter += 1

                graph = get_random_digraph(num_nodes, edge_prob)

                if connected:
                    if nx.is_connected(graph):
                        pass
                    else:
                        continue

                if two_connected:
                    if nx.is_biconnected(graph):
                        pass
                    else:
                        continue

                if distance_hereditary:
                    if is_distance_hereditary(graph):
                        pass
                    else:
                        continue

                if distance_regular:
                    if nx.is_distance_regular(graph):
                        pass
                    else:
                        continue

                if check_free_of:
                    is_free_of = True
                    for sg in forbidden_subgraphs:
                        GM = isomorphism.GraphMatcher(graph, sg)
                        res = GM.subgraph_is_isomorphic()
                        if res:
                            is_free_of = False
                    if not is_free_of:
                        continue

                if check_contains:
                    contains = False
                    for sg in forbidden_subgraphs:
                        GM = isomorphism.GraphMatcher(graph, sg)
                        res = GM.subgraph_is_isomorphic()
                        if res:
                            is_free_of = True
                    if contains:
                        pass
                    else:
                        continue

                pass_filter += 1

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
                        save_transit_function(transit_function_test, outdir + "example_" + str(valid_graphs) + ".tsv", vertices)
                    valid_graphs += 1

# Random Function Mode
elif random_function:

    print("Checking Random Functions on", num_nodes, "vertices.")
    print("-----------------------------------")

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
                    print(counter, "functions checked ...")

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
                    print(counter, "functions checked ...")

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

# If no mode is chosen, iterate over all undirected graphs <= 7 vertices
else:

    print("Checking all graphs up to 7 vertices.")
    print("-----------------------------------")

    graph_atlas = nx.graph_atlas_g()

    if signpost:

        counter = 0
        pass_filter = 0

        for graph in graph_atlas:

            if counter % 100 == 0:
                print()
                print(counter, "graphs checked ...", pass_filter, "passed filtering.")

            counter += 1

            if num_nodes != 0 and len(graph.nodes()) < num_nodes:
                continue

            if len(graph.nodes()) == 0:
                continue

            if connected:
                if nx.is_connected(graph):
                    pass
                else:
                    continue

            if two_connected:
                if nx.is_biconnected(graph):
                    pass
                else:
                    continue

            if distance_hereditary:
                if is_distance_hereditary(graph):
                    pass
                else:
                    continue

            if distance_regular:
                if nx.is_distance_regular(graph):
                    pass
                else:
                    continue

            if check_free_of:
                is_free_of = True
                for sg in forbidden_subgraphs:
                    GM = isomorphism.GraphMatcher(graph, sg)
                    res = GM.subgraph_is_isomorphic()
                    if res:
                        is_free_of = False
                if not is_free_of:
                    continue

            if check_contains:
                contains = False
                for sg in forbidden_subgraphs:
                    GM = isomorphism.GraphMatcher(graph, sg)
                    res = GM.subgraph_is_isomorphic()
                    if res:
                        is_free_of = True
                if contains:
                    pass
                else:
                    continue

            pass_filter += 1

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
                    save_step_function(stepfunction_set,
                                          outdir + "example_" + str(valid_graphs) + ".tsv", vertices)
                valid_graphs += 1

    elif not signpost:

        counter = 0
        pass_filter = 0

        for graph in graph_atlas:

            if counter % 100 == 0:
                print()
                print(counter, "graphs checked ...", pass_filter, "passed filtering.")

            counter += 1

            if num_nodes != 0 and len(graph.nodes()) < num_nodes:
                continue

            if len(graph.nodes()) == 0:
                continue

            if connected:
                if nx.is_connected(graph):
                    pass
                else:
                    continue

            if two_connected:
                if nx.is_biconnected(graph):
                    pass
                else:
                    continue

            if distance_hereditary:
                if is_distance_hereditary(graph):
                    pass
                else:
                    continue

            if distance_regular:
                if nx.is_distance_regular(graph):
                    pass
                else:
                    continue

            if check_free_of:
                is_free_of = True
                for sg in forbidden_subgraphs:
                    GM = isomorphism.GraphMatcher(graph, sg)
                    res = GM.subgraph_is_isomorphic()
                    if res:
                        is_free_of = False
                if not is_free_of:
                    continue

            if check_contains:
                contains = False
                for sg in forbidden_subgraphs:
                    GM = isomorphism.GraphMatcher(graph, sg)
                    res = GM.subgraph_is_isomorphic()
                    if res:
                        is_free_of = True
                if contains:
                    pass
                else:
                    continue

            pass_filter += 1

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
                    save_transit_function(transit_function_test, outdir + "example_" + str(valid_graphs) + ".tsv", vertices)
                valid_graphs += 1



if signpost:
    print()
    print(valid_graphs, "explored step systems satisfied the constraints")
    try:
        print(pass_filter, "passed filtering.")
    except:
        pass
elif not signpost:
    print()
    print(valid_graphs, "explored transit functions satisfied the constraints")
    try:
        print(pass_filter, "passed filtering.")
    except:
        pass
