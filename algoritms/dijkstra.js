// Graph representation
const graph = {
    start: { a: 6, b: 2 },
    a: { meta: 1 },
    b: { a: 3, meta: 5 },
    meta: {}
};

// Function to find the node with the lowest cost
function findLowestCostNode(costs, processed) {
    let lowestCost = Infinity;
    let lowestCostNode = null;

    for (let node in costs) {
        let cost = costs[node];
        if (cost < lowestCost && !processed.includes(node)) {
            lowestCost = cost;
            lowestCostNode = node;
        }
    }

    return lowestCostNode;
}

// Function implementing Dijkstra's algorithm
function dijkstra(graph) {
    // Costs of passing through each node
    const costs = {
        a: 6,
        b: 2,
        meta: Infinity
    };

    // Array of parents
    const parents = {
        a: "start",
        b: "start",
        meta: null
    };

    // Processed nodes
    const processed = [];

    // Find the node with the lowest cost
    let node = findLowestCostNode(costs, processed);

    while (node !== null) {
        let cost = costs[node];
        let neighbors = graph[node];

        for (let neighbor in neighbors) {
            let newCost = cost + neighbors[neighbor];
            if (newCost < costs[neighbor]) {
                costs[neighbor] = newCost;
                parents[neighbor] = node;
            }
        }

        processed.push(node);
        node = findLowestCostNode(costs, processed);
    }

    return { costs, parents };
}

// Running the algorithm
const result = dijkstra(graph);
console.log("Costs:", result.costs);
console.log("Parents:", result.parents);