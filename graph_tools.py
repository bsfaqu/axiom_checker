import networkx as nx

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
                transit_function[(u, v)] = transit_function[(u, v)].union(set(path))

    return transit_function

def step_to_graph(stepfunction_set):

    graph = nx.Graph()

    vertices = set()

    for t in stepfunction_set:
        for e in t:
            vertices.update(e)

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
        vertices.update(k[0])
        vertices.update(k[1])

    for k in transit_function.keys():
        if transit_function[k] == {k[0], k[1]}:
            graph.add_edge(k[0], k[1])