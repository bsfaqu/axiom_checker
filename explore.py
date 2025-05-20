import networkx as nx
from matplotlib import pyplot as plt
from networkx.algorithms import isomorphism
import sys
from sys import argv
from math_strings import *
from graph_tools import *


axiom_strings_transit = [
            "t0", "t1", "t2s", "t2a", "t3",
            "tr2", "b1", "b2", "b3", "b4",
            "b6", "j2", "F", "G", "co0",
            "co1", "co2", "co3", "g", "p",
            "mod", "med", "b5"
        ]

axiom_strings_stepfunctions = [
    "A", "B", "H", "C", "D", "F", "G", "E",
    "Pt", "Dd", "Dt", "Cw", "Cb", "Dm", "T1",
    "T2", "Tb2", "P4", "Sm"
]

signpost = False
csv_file = ""
ax_choice = []
wrong_file_choice = False
no_file = True

for arg in argv:

    # Print help string and exit if help argument was supplied
    if arg in ["-h", "--help", "--manual"]:
        print()
        print("Call check.py with:")
        print("python check.py -a [axioms] -f [filename]")
        print("or")
        print("python check.py --axioms [axioms] --file [filename]")
        print("[axioms] should be axiom strings, comma separated, i.e. 'b1,b5,tr2'")
        print("Please do not include any spaces in the axiom string.")
        print("Stepsystems can be checked by including a -s argument, e.g. ")
        print("python check.py -s -a [axioms] -f [filename]")
        print()
        print("Visualization of G_R/G_T will be saved under the same name as the input file with a .png extension.")
        print()

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
        print("Select (transit function) axioms with:", sstr(axiom_strings_transit))
        print()
        print("Select (step function) axioms with:", sstr(axiom_strings_stepfunctions))
        print()
        sys.exit()

    if arg in ["-s", "--signpost"]:
        signpost = True

    if arg in ["--axioms", "-a"]:
        try:
            ax_choice = argv[argv.index(arg) + 1].split(",")
        except:
            wrong_ax_choice = True

    if arg in ["--file", "-f"]:
        no_file = False
        try:
            csv_file = argv[argv.index(arg) + 1]
        except:
            wrong_file_choice = True


if no_file:
    ga = nx.graph_atlas_g()
    valid_graphs = 0

    for graph in ga:
        pass


if signpost and no_file:
    print(valid_graphs, "step systems satisfied the constraints")
elif not signpost and no_file:
    print(valid_graphs, "transit functions satisfied the constraints")
