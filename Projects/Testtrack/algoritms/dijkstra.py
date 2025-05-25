def _find_lowest_cost_node(costs, processed):
    lowest_cost = float('inf')
    lowest_cost_node = None

    for node in costs:
        cost = costs[node]
        if cost < lowest_cost and node not in processed:
            lowest_cost = cost
            lowest_cost_node = node

    return lowest_cost_node


def dijkstra(graph: dict, costs: dict, parents: dict):
    processed = []
    node = _find_lowest_cost_node(costs, processed)

    while node is not None:
        cost = costs[node]
        neighbors = graph[node]

        for n in neighbors.keys():
            new_cost = cost + neighbors[n]
            if new_cost < costs[n]:
                costs[n] = new_cost
                parents[n] = node

        processed.append(node)
        node = _find_lowest_cost_node(costs, processed)


if __name__ == "__main__":
    graph = {
        "start": {"a": 6, "b": 2},
        "a": {"meta": 1},
        "b": {"a": 3, "meta": 5},
        "meta": {}
    }
    costs = {
        "a": 6,
        "b": 2,
        "meta": float('inf')
    }
    parents = {
        "a": "start",
        "b": "start",
        "meta": None
    }

    dijkstra(graph, costs, parents)

    print("Costs:", costs)
    print("Parents:", parents)
