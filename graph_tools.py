import matplotlib.pyplot as plt
import networkx as nx
from math_strings import *

# TODO Include vertices in the functions?

def graph_to_step(graph):

    stepsystem = []

    for u in graph.nodes():
        for v in graph.nodes():
            if u == v:
                continue
            try:
                paths = list(nx.all_shortest_paths(graph, source=u, target=v))
            except:
                continue

            for p in paths:
                stepsystem += [(u, p[1], v)]

    return set(stepsystem)

def graph_to_transit(graph):

    transit_function = dict()

    for u in graph.nodes():
        for v in graph.nodes():
            if u == v:
                transit_function[(u, v)] = {u}
            else:
                transit_function[(u, v)] = set()

    for u in graph.nodes():
        for v in graph.nodes():
            if u == v:
                continue
            try:
                paths = list(nx.all_shortest_paths(graph, source=u, target=v))
            except:
                continue

            for p in paths:
                transit_function[(u, v)] = transit_function[(u, v)].union(set(p))

    return transit_function

def step_to_graph(stepfunction_set):

    graph = nx.Graph()

    vertices = set()

    for t in stepfunction_set:
        for e in t:
            vertices.update([e])

    for v in vertices:
        graph.add_node(v)

    for t in stepfunction_set:
        if t[1] == t[2]:
            graph.add_edge(t[0], t[2])

    return graph

def transit_to_graph(transit_function):

    graph = nx.DiGraph()

    vertices = set()

    for k in transit_function.keys():
        vertices.update([k[0]])
        vertices.update([k[1]])

    for k in transit_function.keys():
        if transit_function[k] == {k[0], k[1]}:
            graph.add_edge(k[0], k[1])

    return graph

def save_graph(graph, outfile):
    nx.draw(graph, with_labels=True)
    plt.savefig(outfile)
    plt.close()
    print("Saved graph to", outfile)


def save_transit_function(transit_function, outfile, vertices):
    vertices = list(vertices)

    tsv_list = [["*" for j in range(len(vertices) + 1)] for i in range(len(vertices) + 1)]
    tsv_list[0][0] = ""

    for i in range(1, len(vertices)+1):
        tsv_list[0][i] = str(vertices[i-1])
        tsv_list[i][0] = str(vertices[i-1])

    for i in range(1, len(vertices) + 1):
        for j in range(1, len(vertices) + 1):
            tsv_list[i][j] = sstr(transit_function[(vertices[i-1], vertices[j-1])]).replace("}","").replace("{","").replace(" ","").replace("∅", "")

    out_string = ""

    for line in tsv_list:
        for col in line:
            out_string += col + "\t"
        out_string = out_string[0:-1] + "\n"

    out_string = out_string[0:-1]
    with open(outfile, "w+") as f:
        f.write(out_string)

def save_step_function(stepfunction, outfile, vertices):
    vertices = list(vertices)

    tsv_list = [["*" for j in range(len(vertices) + 1)] for i in range(len(vertices) + 1)]
    tsv_list[0][0] = ""

    for i in range(1, len(vertices) + 1):
        tsv_list[0][i] = str(vertices[i - 1])
        tsv_list[i][0] = str(vertices[i - 1])

    for i in range(1, len(vertices) + 1):
        for j in range(1, len(vertices) + 1):
            matching_vertices = [t[1] for t in stepfunction if t[0] == vertices[i - 1] and t[2] == vertices[j - 1]]
            tsv_list[i][j] = sstr(matching_vertices).replace("}", "").replace("{","").replace(" ", "").replace("∅", "")

    out_string = ""

    for line in tsv_list:
        for col in line:
            out_string += col + "\t"
        out_string = out_string[0:-1] + "\n"

    out_string = out_string[0:-1]
    with open(outfile, "w+") as f:
        f.write(out_string)
