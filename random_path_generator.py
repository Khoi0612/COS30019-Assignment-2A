import random
import os
import matplotlib.pyplot as plt

def random_graph():

    # Generate random nodes of coordinates from 1 - 10
    nodes = {}
    for i in range(10):
     nodes.setdefault(i + 1, (random.randint(0, 10), random.randint(0, 10)))

    # Generate random edges from random nodes with random costs
    edges = {}
    for node in nodes:
        number_of_connected_nodes = random.randint(1, 3) # Number of nodes that can be visted from current node
        connected_count = 0 # Number of nodes that have been connected
        while connected_count < number_of_connected_nodes:
            connected_node = random.randint(1, len(nodes)) # Randomized which node can be visited
            cost_forward = random.randint(1, 10) # Randomized cost
            directed = bool(random.getrandbits(1)) # Randomized whether the edge is directed
            
            # Avoid self-connected: {(x,x):c}
            if connected_node == node:
                continue

            # Avoid duplicate edges with potentially different cost: {(x,y):c1, (x,y):c2}    
            if (node, connected_node) not in edges and (connected_node, node) not in edges:
                edges[(node, connected_node)] = cost_forward
                connected_count += 1
                
                if not directed:
                    cost_backward = random.randint(1, 10) # Cost backward can be different from cost forward
                    edges[(connected_node, node)] = cost_backward

    # Generate random origin node
    origin=random.randint(1, len(nodes))

    # Generate random destinations list
    number_of_destinations=random.randint(1, 5) # Randomize the number of destination in the list
    destinations=list()
    while len(destinations) < number_of_destinations:
        destination=random.choice(list(nodes.keys())) # Choose random node to be a destination

        # Avoide duplicate detination and destination being the origin
        if destination != origin and destination not in destinations:
            destinations.append(destination)

    # Convert nodes dictionary to string
    nodes_str="Nodes:\n"
    for node, coor in nodes.items():
        node_str=f"{node}: ({coor[0]},{coor[1]})\n" # 1: (2,3)
        nodes_str+=node_str

    # Convert edges dictionary to string
    edges_str="Edges:\n"
    for edge, node in edges.items():
        edge_str=f"({edge[0]},{edge[1]}): {node}\n" # (1,2): 3
        edges_str+=edge_str

    # Convert origin to string
    origin_str=f"Origin:\n{origin}\n"

    # Convert destinations list to string
    dests_str="Destinations:\n"
    for dest in destinations: # If it isn't the last element
        if dest is not destinations[-1]:
            dest_str=f"{dest}; " # 1; 2; ..
        else:
            dest_str=f"{dest}" # ;.. 3
        dests_str+=dest_str

    text_file_str=nodes_str+edges_str+origin_str+dests_str

    return  nodes, edges, origin, destinations, text_file_str

def export_graph(content, base_name="test_"):

    # Export a string to a text file with incrementing filename
    i = 1 # Starting index
    while True:
        extension = ".txt" # Text file
        filename = f"{base_name}{i}{extension}"

        # If file not exist, create file and end loop
        if not os.path.exists(filename):
            with open(filename, "w") as file:
                file.write(content)
            print(f"Exported to {filename}")
            break
        
        # If it exist, increment index and start again
        i += 1

    return filename

def draw_graph(vertices, edges, origin, destinations, title):

    # Set up Figure
    fig, ax = plt.subplots(figsize=(8, 8))

    # Set up Grid
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    plt.grid(True)
    ax.set_aspect('equal')
    
    # Draw vertices
    for name, (x, y) in vertices.items():
        if name == origin:
            color = 'limegreen'
        elif name in destinations:
            color = 'orange'
        else:
            color = 'skyblue'

        ax.plot(x, y, 'o', markersize=10, color=color)  # Higher zorder to display on top
        label = str(name)
        if name == origin:
            label += " (Origin)"
        elif name in destinations:
            label += " (Dest)"
        ax.text(x + 0.1, y + 0.1, label, fontsize=12, 
               bbox=dict(facecolor='white', alpha=0.7, edgecolor='none'),
               zorder=4)  # Text with background

    # Draw edges
    edge_set = set(edges.keys())
    drawn = set() # Track whether the edge has been drawn 
    for (src, dst) in edges.keys():
        x0, y0 = vertices[src]
        x1, y1 = vertices[dst]
        
        if (dst, src) in edge_set and (dst, src) not in drawn:
            # Undirected
            ax.plot([x0, x1], [y0, y1], 'k-', lw=1.5)
            ax.plot(x0, y0, 'o', markersize=5, color='black')
            ax.plot(x1, y1, 'o', markersize=5, color='black')

        elif (dst, src) not in edge_set:
            # Directed
            ax.annotate("",
                       xy=(x1, y1), xycoords='data',
                       xytext=(x0, y0), textcoords='data',
                       arrowprops=dict(arrowstyle="->", color='black', lw=1.5, mutation_scale=20))

        drawn.add((src, dst))

    plt.title(title)
    plt.show()


def runGenerator():

    # Extract components from randomized graph
    map_nodes, map_edges, map_origin, map_dests, map_str = random_graph()

    # Extraxt title from exported filename
    filename = export_graph(map_str).removesuffix(".txt")
    title = f"Graph {filename}"

    # Draw graph
    draw_graph(map_nodes, map_edges, map_origin, map_dests, title)

runGenerator()