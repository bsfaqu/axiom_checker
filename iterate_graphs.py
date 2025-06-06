import networkx as nx
from matplotlib import pyplot as plt
from networkx.algorithms import isomorphism
import sys
from math_strings import *


def Sm(u, v, w, x, y, z, stepfunction):
    cond_0 = (v, w, x) in stepfunction
    cond_1 = (v, w, z) in stepfunction
    cond_2 = (x, y, z) in stepfunction

    impl_0 = (v, w, y) in stepfunction

    if (cond_0 and cond_1 and cond_2) and not (impl_0):
        # print("VIOLATE (Sm)")
        # print("u ", "->", u, ", v", "->", v, ", w", "->", w, ", x", "->", x, ", y", "->", y, ", z", "->", z)
        # print(tp(v, w, x), elem(), T(), aand(), tp(v, w, z), elem(), T(), aand(), tp(x, y, z), elem(), T(),
        #       nimplies(), tp(v, w, y), elem(), T())
        # print("---")
        return False
    return True


def get_stepfunction(graph):

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

    return stepsystem

ga = nx.graph_atlas_g()

valid_graphs = 0

fan = nx.Graph()

fan.add_node(0)
fan.add_node(1)
fan.add_node(2)
fan.add_node(3)
fan.add_node(4)

fan.add_edge(0, 1)
fan.add_edge(0, 2)
fan.add_edge(0, 3)
fan.add_edge(0, 4)

fan.add_edge(1, 2)
fan.add_edge(2, 3)
fan.add_edge(3, 4)

nx.draw(fan)
plt.savefig("3-fan.png")


count = nx.Graph()

count.add_node(0)
count.add_node(1)
count.add_node(2)
count.add_node(3)
count.add_node(4)

count.add_edge(0, 4)
count.add_edge(0, 3)
count.add_edge(1, 4)
count.add_edge(1, 3)
count.add_edge(2, 4)
count.add_edge(2, 3)
count.add_edge(4, 3)


# fan2 = nx.Graph()
#
# fan2.add_node(0)
# fan2.add_node(1)
# fan2.add_node(2)
# fan2.add_node(3)
# fan2.add_node(4)
# fan2.add_node(5)
#
# fan2.add_edge(0, 1)
# fan2.add_edge(0, 2)
# fan2.add_edge(0, 3)
# fan2.add_edge(0, 4)
#
# fan2.add_edge(1, 2)
# fan2.add_edge(2, 3)
# fan2.add_edge(3, 4)
# fan2.add_edge(5, 4)
# fan2.add_edge(5, 1)
#
# GM = isomorphism.GraphMatcher(fan2, fan)
# res = GM.subgraph_is_isomorphic()
# print(res)


for graph in ga:
    if len(graph.nodes()) < 5:
        pass
    else:
        if nx.is_chordal(graph):
            if len(list(nx.connected_components(graph))) == 1:
                GM = isomorphism.GraphMatcher(graph, fan)
                res = GM.subgraph_is_isomorphic()
                if res:
                    continue
                else:
                    valid_graphs += 1
                    stepfunction = get_stepfunction(graph)
                    vertices = list(graph.nodes)

                    stop_graph = False

                    for u in vertices:
                        if stop_graph:
                            break
                        for v in vertices:
                            if stop_graph:
                                break
                            for w in vertices:
                                if stop_graph:
                                    break
                                for x in vertices:
                                    if stop_graph:
                                        break
                                    for y in vertices:
                                        if stop_graph:
                                            break
                                        for z in vertices:
                                            if stop_graph:
                                                break
                                            is_smooth = Sm(u, v, w, x, y, z, stepfunction)
                                            if not is_smooth:

                                                GM = isomorphism.GraphMatcher(graph, count)
                                                res = GM.subgraph_is_isomorphic()

                                                if res:
                                                    stop_graph = True
                                                    break

                                                print("NOT SMOOTH GRAPH NR", valid_graphs)
                                                print(vertices)
                                                print(list(graph.edges()))
                                                print("---------------")
                                                stop_graph = True

print(valid_graphs)