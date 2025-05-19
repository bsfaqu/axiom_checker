import sys
from sys import argv

for arg in sys.argv:
    if arg in ["-h", "--help", "--manual"]:
        print()
        print("Call make_tsv.py with:")
        print("python make_tsv.py [vertices] [output-filename]")
        print("For example, 'python make_tsv.py u,v,w example.tsv' will create the following file:")
        print("\tu\tv\tw")
        print("u\t*\t*\t*")
        print("v\t*\t*\t*")
        print("w\t*\t*\t*")
        print()
        print()
        print("Transit Functions:")
        print("-------------------")
        print("The desired transit sets R(u, v), etc.,  are filled into the generated .tsv files. ")
        print("The format is R([column], [row]), filled into the corresponding fields of the .tsv.")
        print("For example, the interval function of a P3->, R(u, v)={u, v}, R(v, w)={v, w}, R(u, w)={u, v, w} with "
              "the rest of the transit sets being empty can be described with the following .tsv:")
        print("\tu\tv\tw")
        print("u\t*\tu,v\tu,v,w")
        print("v\t*\t*\tv,w")
        print("w\t*\t*\t*")
        print()
        print("The * placeholder in the .tsv signal check.py to fill 'missing' transit sets with the "
              "interval function on G_R. For example, P3-> can also be described with the following .tsv, where "
              "the transit set R(u, w) will be generated on-the-fly by using the interval function on G_R:")
        print("\tu\tv\tw")
        print("u\t*\tu,v\t*")
        print("v\t*\t*\tv,w")
        print("w\t*\t*\t*")
        print()
        print("Take note that the empty string '' (not including the quotation marks) can be used to force empty "
              "transit sets for a pair of vertices, i.e.")
        print("\tu\tv\tw")
        print("u\t*\tu,v\t")
        print("v\t*\t*\tv,w")
        print("w\t*\t*\t*")
        print("which, in this case, leads to the transit function not to be graphic.")
        print()
        print()
        print("Step Functions:")
        print("---------------")
        print("Step functions are provided in a similar format and are generated with the same command as described "
              "above.")
        print("For every comma separated [step] entry in a [col], [row] field in the .tsv, a triple ([col],[step],[row]) "
              "is derived.")
        print("For example, in check.py the step function {(u, v, v), (u, v, w), (v, w, w), (w, v, v), (w, v, u)} is "
              "generated from the following .tsv:")
        print("\tu\tv\tw")
        print("u\t*\tv\tv")
        print("v\tu\t*\tw")
        print("w\tv\tv\t*")
        print()
        print("In a similar fashion as for transit function, fields with * will be populated with steps derived "
              "from the shortest paths in G_T. Again, these steps can be forced to be empty by setting the field to "
              "an empty string '' (not including the quotation marks).")
        print("For example, the step function above can also be generated with:")
        print("\tu\tv\tw")
        print("u\t*\tv\t*")
        print("v\t*\t*\tw")
        print("*\t*\t*\t*")
        print()
        sys.exit()

vertices_list = argv[1].split(",")
outfile = argv[2]

tsv_str = "\t"
vertices = len(vertices_list)

for v in vertices_list:
    tsv_str += v + "\t"
tsv_str = tsv_str[0:-1]
tsv_str += "\n"


for i in range(vertices):
    tsv_str += vertices_list[i] + "\t"
    for j in range(vertices):
        tsv_str += "*" + "\t"
    tsv_str = tsv_str[0:-1]
    tsv_str += "\n"

print(tsv_str)

with open(outfile, "w+") as f:
    f.write(tsv_str)