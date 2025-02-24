import osmnx as ox
import networkx as nx
import matplotlib.pyplot as plt
from pyproj import Transformer
import random


def transform_coordinates(lat, lon, graph_crs):
    transformer = Transformer.from_crs("epsg:4326", graph_crs, always_xy=True)
    return transformer.transform(lon, lat)


def plot_route(graph, paths, colors, title, distances=None, show_nodes=False):
    # Force dark theme for Matplotlib
    plt.style.use("dark_background")

    fig, ax = ox.plot_graph(graph, show=False, close=False, bgcolor="black", node_size=0, edge_color="gray")

    # Ensure background stays black
    fig.patch.set_facecolor("black")
    ax.set_facecolor("black")

    # Plot routes
    for i, (path, color) in enumerate(zip(paths, colors)):
        route_x = [graph.nodes[node]['x'] for node in path]
        route_y = [graph.nodes[node]['y'] for node in path]

        label = f"Path {i + 1}"
        if distances and i < len(distances):
            label += f" ({distances[i]:.2f}km)"

        ax.plot(route_x, route_y, c=color, linewidth=2, label=label)

        if show_nodes:
            for node in path:
                ax.scatter(graph.nodes[node]['x'], graph.nodes[node]['y'], c="white", s=10)

    # Set title with white color
    plt.title(title, fontsize=16, color="white", pad=20, weight='bold')

    # Customize legend for dark theme
    legend = plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=10, facecolor="black", edgecolor="white")
    for text in legend.get_texts():
        text.set_color("white")

    plt.tight_layout()
    plt.show()


def calculate_path_length(graph, path, weight='length'):
    return sum(graph[path[i]][path[i + 1]][0][weight] for i in range(len(path) - 1))


def calculate_prm_alternative_paths(graph, source, target, k=3):
    alternative_paths = []
    attempts = 0
    max_attempts = 10

    while len(alternative_paths) < k and attempts < max_attempts:
        sampled_graph = graph.copy()
        edges_to_remove = random.sample(list(sampled_graph.edges), int(len(sampled_graph.edges) * 0.15))

        for edge in edges_to_remove:
            sampled_graph.remove_edge(*edge)
            if not nx.has_path(sampled_graph, source, target):
                sampled_graph.add_edge(*edge)

        if nx.has_path(sampled_graph, source, target):
            alt_path = nx.shortest_path(sampled_graph, source=source, target=target, weight='length')
            if not alternative_paths or all(
                    len(set(alt_path) - set(p)) > len(alt_path) * 0.3 for p in alternative_paths):
                alternative_paths.append(alt_path)
                path_length = calculate_path_length(graph, alt_path) / 1000  # Convert to km
                print(
                    f"[DEBUG] Found PRM path {len(alternative_paths)} with {len(alt_path)} nodes, {path_length:.2f}km")

        attempts += 1

    return alternative_paths


def simulate_traffic_updates(graph, original_path):
    path_nodes = set(original_path)
    major_intersections = [node for node in path_nodes
                           if len(list(graph.predecessors(node))) > 2]

    updates = []
    for node in major_intersections:
        neighbors = list(graph.successors(node))
        for neighbor in neighbors:
            if graph.has_edge(node, neighbor):
                base_length = graph[node][neighbor][0]['length']
                traffic_penalty = base_length * random.uniform(3, 8)
                graph[node][neighbor][0]['length'] += traffic_penalty
                updates.append(((node, neighbor), traffic_penalty))

    other_edges = random.sample([e for e in graph.edges if e[0] not in path_nodes], 15)
    for edge in other_edges:
        if graph.has_edge(*edge):
            base_length = graph[edge[0]][edge[1]][0]['length']
            traffic_penalty = base_length * random.uniform(1.5, 3)
            graph[edge[0]][edge[1]][0]['length'] += traffic_penalty
            updates.append((edge, traffic_penalty))

    return updates


def simulate():
    print("[DEBUG] Starting Manhattan emergency route simulation...")

    # Display input instructions
    print("Enter coordinates in the format: latitude, longitude (e.g., 40.823479, -73.936095).")
    print("Leave blank to use default coordinates:\n"
          " - Source: Harlem (40.823479, -73.936095)\n"
          " - Destination: Hospital (40.710148, -74.004925)\n")

    # Get custom coordinates or use defaults
    try:
        source_coords = input("Enter source coordinates (latitude, longitude): ").strip()
        target_coords = input("Enter destination coordinates (latitude, longitude): ").strip()

        if source_coords:
            harlem_coords = tuple(map(float, source_coords.split(',')))
        else:
            print("Using default source coordinates: Harlem (40.823479, -73.936095)")
            harlem_coords = (40.823479, -73.936095)

        if target_coords:
            hospital_coords = tuple(map(float, target_coords.split(',')))
        else:
            print("Using default destination coordinates: Hospital (40.710148, -74.004925)")
            hospital_coords = (40.710148, -74.004925)

    except ValueError:
        print("[ERROR] Invalid input detected. Using default coordinates.")
        harlem_coords = (40.823479, -73.936095)
        hospital_coords = (40.710148, -74.004925)

    # Load and project the graph
    manhattan = ox.graph_from_place("Manhattan, New York City, New York, USA", network_type="drive")
    manhattan = ox.project_graph(manhattan)

    # Transform coordinates to graph CRS
    harlem_x, harlem_y = transform_coordinates(*harlem_coords, manhattan.graph['crs'])
    hospital_x, hospital_y = transform_coordinates(*hospital_coords, manhattan.graph['crs'])

    # Find nearest nodes to the input coordinates
    harlem_node = ox.distance.nearest_nodes(manhattan, X=harlem_x, Y=harlem_y)
    hospital_node = ox.distance.nearest_nodes(manhattan, X=hospital_x, Y=hospital_y)

    # Dijkstra's Algorithm Path
    dijkstra_path = nx.shortest_path(manhattan, harlem_node, hospital_node, weight="length")
    dijkstra_cost = calculate_path_length(manhattan, dijkstra_path)
    print(f"[DEBUG] Dijkstra path found: {len(dijkstra_path)} nodes, {dijkstra_cost / 1000:.2f}km")
    plot_route(manhattan, [dijkstra_path], ["red"],
               f"Dijkstra's Algorithm - Shortest Path\nDistance: {dijkstra_cost / 1000:.2f}km",
               distances=[dijkstra_cost / 1000])

    # PRM Alternative Paths
    prm_paths = calculate_prm_alternative_paths(manhattan, harlem_node, hospital_node, k=3)
    if prm_paths:
        distances = [calculate_path_length(manhattan, path) / 1000 for path in prm_paths]
        title = "PRM Alternative Routes\n" + \
                "Multiple paths with varying distances"
        plot_route(manhattan, prm_paths, ["yellow", "orange", "pink"][:len(prm_paths)],
                   title, distances=distances, show_nodes=True)

    # Waze-like Dynamic Routing
    simulate_traffic_updates(manhattan, dijkstra_path)
    waze_path = nx.shortest_path(manhattan, harlem_node, hospital_node, weight="length")
    waze_cost = calculate_path_length(manhattan, waze_path)
    print(f"[DEBUG] Dynamic route found: {len(waze_path)} nodes, {waze_cost / 1000:.2f}km")
    plot_route(manhattan, [waze_path], ["blue"],
               f"Dynamic (Waze-like) Routing\nDistance with traffic: {waze_cost / 1000:.2f}km",
               distances=[waze_cost / 1000])



if __name__ == "__main__":
    simulate()