from p1_support import load_level, show_level, save_level_costs
import math
from math import inf, sqrt
from heapq import heappop, heappush


def dijkstras_shortest_path(initial_position, destination, graph, adj):
    """ Searches for a minimal cost path through a graph using Dijkstra's algorithm.

    Args:
    Returns:
    If a path exits, return a list containing all cells from initial_position to destination.
    Otherwise, return None.

    """

    #Data Structures initialized
    dist = {}
    prev = {}
    queue = []
    path = []

    dist[initial_position] = 0.0
    prev[initial_position] = None

    heappush(queue,(dist[initial_position], initial_position))


    while len(queue) > 0:

        cost, minnode = heappop(queue)
        if(minnode == destination):
            break

        nodes = adj(graph, minnode)
        nodes.sort()
        for node in nodes:
            alt = dist[minnode] + node[0]
            if (node[1] not in dist) or alt < dist[node[1]]:
                dist[node[1]] = alt
                prev[node[1]] = minnode
                heappush(queue,(alt,node[1]))
    if minnode == destination:
        while minnode:
            path.append(prev[minnode])
            minnode = prev[minnode]
        path.reverse()
        return path
    else:
        return []
    pass


def dijkstras_shortest_path_to_all(initial_position, graph, adj):
    """ Calculates the minimum cost to every reachable cell in a graph from the initial_position.

    Args:
        initial_position: The initial cell from which the path extends.
        graph: A loaded level, containing walls, spaces, and waypoints.
        adj: An adjacency function returning cells adjacent to a given cell as well as their respective edge costs.

    Returns:
        A dictionary, mapping destination cells to the cost of a path from the initial_position.
    """
    dist = {}
    prev = {}
    queue = []

    dist[initial_position] = 0.0
    prev[initial_position] = None
    heappush(queue,(dist[initial_position], initial_position))

    while len(queue) > 0:
        cost, minnode = heappop(queue)
        nodes = adj(graph, minnode)
        nodes.sort()
        for node in nodes:
            alt = dist[minnode] + node[0]
            if node[1] not in dist or alt < dist[node[1]]:
                dist[node[1]] = alt
                prev[node[1]] = minnode
                heappush(queue,(alt, node[1]))
    return dist
    pass


def navigation_edges(level, cell):
    """ Provides a list of adjacent cells and their respective costs from the given cell.

        Args:
            level: A loaded level, containing walls, spaces, and waypoints.
            cell: A target location.

        Returns:
            A list of tuples containing an adjacent cell's coordinates and the cost of the edge joining it and the
            originating cell.

            E.g. from (0,0):
                [((0,1), 1),
                 ((1,0), 1),
                 ((1,1), 1.4142135623730951),
                 ... ]
    """
    a = cell[0]
    b = cell[1]
    adjList = []

    for i in range (a-1, a+2):
        for j in range(b-1, b+2):
            if (i, j) in level['walls']:
                pass
            elif (i, j) == cell:
                pass
            else:
                if (i == a-1 and j == b-1) or (i == a-1 and j == b+1) or (i == a+1 and j == b-1) or (i == a+1 and j == b+1):
                    newCost = .5*math.sqrt(2)*level['spaces'][(a, b)] + .5*math.sqrt(2)*level['spaces'][(i, j)]
                    adjList.append((newCost, (i, j)))
                else:
                    newCost = .5*level['spaces'][(a,b)] + .5*level['spaces'][(i, j)]
                    adjList.append((newCost, (i, j)))
    return adjList
    pass



def test_route(filename, src_waypoint, dst_waypoint):
    """ Loads a level, searches for a path between the given waypoints, and displays the result.

    Args:
        filename: The name of the text file containing the level.
        src_waypoint: The character associated with the initial waypoint.
        dst_waypoint: The character associated with the destination waypoint.

    """

    # Load and display the level.
    level = load_level(filename)
    show_level(level)

    # Retrieve the source and destination coordinates from the level.
    src = level['waypoints'][src_waypoint]
    dst = level['waypoints'][dst_waypoint]

    # Search for and display the path from src to dst.
    path = dijkstras_shortest_path(src, dst, level, navigation_edges)
    if path:
        show_level(level, path)
    else:
        print("No path possible!")


def cost_to_all_cells(filename, src_waypoint, output_filename):
    """ Loads a level, calculates the cost to all reachable cells from
    src_waypoint, then saves the result in a csv file with name output_filename.

    Args:
        filename: The name of the text file containing the level.
        src_waypoint: The character associated with the initial waypoint.
        output_filename: The filename for the output csv file.

    """

    # Load and display the level.
    level = load_level(filename)
    show_level(level)

    # Retrieve the source coordinates from the level.
    src = level['waypoints'][src_waypoint]

    # Calculate the cost to all reachable cells from src and save to a csv file.
    costs_to_all_cells = dijkstras_shortest_path_to_all(src, level, navigation_edges)
    save_level_costs(level, costs_to_all_cells, output_filename)


if __name__ == '__main__':
    filename, src_waypoint, dst_waypoint = 'test_maze.txt', 'a', 'e'

    # Use this function call to find the route between two waypoints.
    test_route(filename, src_waypoint, dst_waypoint)

    # Use this function to calculate the cost to all reachable cells from an origin point.
    cost_to_all_cells(filename, src_waypoint, 'my_costs.csv')
