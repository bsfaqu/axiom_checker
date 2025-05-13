from sys import argv

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