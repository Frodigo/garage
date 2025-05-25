from collections import deque


def _person_is_seller(name: str) -> bool:
    """
    Checks is person is a seller. In this example, anyone whom name ends on "m" letter is a seller
    """
    return name[-1] == 'm'


def bfs(start: str, graph: dict) -> str:
    """
    Performs a breadth-first search on the given graph starting from the specified start node.

    Args:
        start (str): The key of the start node of the search.
        graph (dict): A dictionary representing the graph, where each key is a node and each value is a list of neighboring nodes.

    Returns:
        str: A string indicating whether a seller was found or not.
    """
    search_queue = deque()
    search_queue += graph[start]

    while search_queue:
        person = search_queue.popleft()
        if _person_is_seller(person):
            return f"Person {person} is a seller"
        else:
            search_queue += graph[person]

    return "No seller found here"


if __name__ == "__main__":
    graph = {
        "ty": ["alice", "bob", "claire"],
        "alice": ["peggy"],
        "bob": ["anuj", "peggy"],
        "claire": ["thom", "jonny"],
        "anuj": [],
        "peggy": [],
        "thom": [],
        "jonny": []
    }

    print(bfs("ty", graph))
