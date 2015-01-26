import graphs

class NotDAG(Exception):
    pass

def topological_sorting(edges_list):
    """
    >>> [(1, 2), (1, 3), (2, 4), (3, 4)]
    None
    """
    graph = graphs.Graph.from_tuple_list(edges_list, directed=True)

    print(graph)

    visited = set()
    top_order = []

    def dfs(v, stack, parents):
        if v not in visited:
            visited.add(v)
            edges = graph.get_edges(v=v)

            if not edges:
                # sink vertex
                stack.insert(0, v)
            else:
                for edge in edges:
                    if edge.to in parents:
                        raise NotDAG
                    parents.add(v)
                    dfs(edge.to, stack, parents)
                parents.remove(v)
                stack.insert(0, v)

    try:
        for v in graph.vertices_list:
            dfs(v, top_order, set()) 
    except NotDAG:
        print("Not a DAG")
        top_order = None

    return top_order

if __name__ == "__main__":
    # import doctest
    # doctest.testmod()
    sample = [(1, 2), (1, 3), (2, 4), (3, 4)]
    print(topological_sorting(sample))

    sample = [(1, 2), (2, 3), (2, 4), (3, 4), (4, 5), (4, 1)]
    print(topological_sorting(sample))

    sample = [(1, 2), (2, 3), (2, 4), (4, 5)]
    print(topological_sorting(sample))
