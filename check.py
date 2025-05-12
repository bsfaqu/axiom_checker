from sys import argv
import sys
from math_strings import *
import transit_function

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
    "T2", "Tb2", "P4"
]

signpost = False

for arg in argv:

    # Print help string and exit if help argument was supplied
    if arg in ["-h", "--help", "--manual"]:
        print()
        print("Call check.py with:")
        print("python check.py -a [axioms] -f [filename]")
        print("or")
        print("python check.py --axioms [axioms] --file [filename]")
        print("[axioms] should by axiom strings, comma separated, i.e. 'b1,b5,tr2'")
        print("Please do not include any spaces in the axiom string.")
        print("Stepsystems can be checked by including a -s argument, e.g. ")
        print("python check.py -s -a [axioms] -f [filename]")
        print()
        print("Supported Axioms (Transit Functions):")
        for a in axiom_strings_transit:
            print_axiom_info(a)
            print()
        print()
        print("Select axioms with:", sstr(axiom_strings_transit))
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
        try:
            csv_file = argv[argv.index(arg) + 1]
        except:
            wrong_file_choice = True

# Check if the axioms supplied are actually supported for signposts and exit otherwise
if signpost:
    not_supported_axioms = []
    for a in ax_choice:
        if a not in axiom_strings_stepfunctions:
            not_supported_axioms += [a]

    if not_supported_axioms != []:
        print("Axioms", sstr(not_supported_axioms), "are not supported for Stepfunctions. ",
                                                    "Please alter your axiom string.")
        sys.exit()

# Check if the axioms supplied are actually supported for DTF and exit otherwise
if not signpost:
    not_supported_axioms = []
    for a in ax_choice:
        if a not in axiom_strings_transit:
            not_supported_axioms += [a]

    if not_supported_axioms != []:
        print("Axioms", sstr(not_supported_axioms), "are not supported for Directed Transit Functions. ",
              "Please alter your axiom string.")
        sys.exit()

# Read some basic input
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


# Output vertices for sanity checking
print()
print("*** VERTICES ***")
print(sstr(vertices))

if not signpost:
    check_object = transit_function.transit_function(csv_lines)

# Axiom checking output
print("\n---\n")
print("*** Axiom checking ***")

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

check_object.check_axioms(ax_choice)

check_object.check_graphic()

check_object.save_graph(csv_file)
