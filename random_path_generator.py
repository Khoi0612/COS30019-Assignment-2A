import random
import os
import sys
import tkinter as tk
from graph_gui import *
import math

def random_graph():

    # Generate random nodes of coordinates from 1 - 10
    nodes = {}
    i = 0
    while i < 5:
        x = random.randint(0, 10)
        y = random.randint(0, 10)
        if (x, y) not in list(nodes.keys()):
            nodes.setdefault(i + 1, (x, y))
            i+=1

    # Generate random edges from random nodes with random costs
    edges = {}
    for node, (x0, y0) in nodes.items():
        # Avoid self-connected: {(x,x):c} and duplicate edges with potentially different cost: {(x,y):c1, (x,y):c2} 
        possible_nodes = [n for n in nodes if n != node and (node, n) not in edges and (n, node) not in edges]
        random.shuffle(possible_nodes)  # Randomize connection order
        
        number_of_connected_nodes = min(random.randint(0, 3), len(possible_nodes))
        
        for i in range(number_of_connected_nodes):
            connected_node = possible_nodes[i]
            (x1, y1) = nodes[connected_node]
            distance = math.sqrt((x1 - x0)**2 + (y1 - y0)**2)
            cost_forward = math.ceil(distance)*2
            different_cost = bool(random.getrandbits(1))
            directed = bool(random.getrandbits(1))

            edges[(node, connected_node)] = cost_forward
            
            if not directed:
                cost_backward = cost_forward if different_cost else cost_forward + 1
                edges[(connected_node, node)] = cost_backward

    # Generate random origin node
    origin=random.randint(1, len(nodes))

    # Generate random destinations list
    number_of_destinations=random.randint(1, len(nodes) - 3) # Randomize the number of destination in the list
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


def runGenerator():
    no_of_tests = int(sys.argv[1])
    i = 0
    maps = {}

    # Looping through the number of tests generated
    while i < no_of_tests:

        # Extract components from randomized graph
        map_nodes, map_edges, map_origin, map_dests, map_str = random_graph()

        # Extraxt title from exported filename
        filename = export_graph(map_str).removesuffix(".txt")
        title = f"Graph {filename}"

        # Appends the components into the dictionary
        maps[i + 1] = dict(nodes = map_nodes, 
                           edges = map_edges,
                           origin = map_origin,
                           dests = map_dests,
                           title = title) # {1:{nodes:A, edges:B, ...}, 2:{...}, ...}       

        # Increment index
        i+=1

    # Extract whether users wants to draw the generated graph
    if len(sys.argv) > 2:
        if sys.argv[2] == "-d":

            # Initiate Tkinter root
            root = tk.Tk()
            app = GraphGUI(root)
            
            # Draw graph for each item in dictionary 
            for id, map in maps.items():               
                app.draw_graph(map["nodes"], map["edges"], map["origin"], map["dests"], map["title"])           

            # Stop the program after the app closed    
            root.protocol("WM_DELETE_WINDOW", app.on_closing)

            # Start Tkinter event loop
            root.mainloop()

runGenerator()