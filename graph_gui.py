import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import sys
from matplotlib import gridspec

class GraphGUI:
    def __init__(self, root, canvas_width=900, canvas_height=700, nav_height=50):
        self.root = root
        self.root.title("Graph GUI")
        self.root.geometry(f"{canvas_width}x{canvas_height + nav_height + 40}")

        # Initialize dimensions
        self.canvas_width = canvas_width
        self.canvas_height = canvas_height
        self.nav_height = nav_height
        
        # List to store all graph data
        self.graphs = []
        self.current_page = 0
        
        # Main frame
        self.main_frame = ttk.Frame(root, padding=10)
        self.main_frame.pack(fill=tk.BOTH, expand=True)        
        
        # Canvas for displaying graphs
        self.canvas_frame = ttk.Frame(self.main_frame, width=canvas_width, height=canvas_height)
        self.canvas_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        self.canvas_frame.pack_propagate(False)
        
        # Navigation frame
        self.nav_frame = ttk.Frame(self.main_frame, height=nav_height)
        self.nav_frame.pack(fill=tk.X, pady=10)
        self.nav_frame.pack_propagate(False)

        # Create a center-aligned container for buttons
        self.button_container = ttk.Frame(self.nav_frame)
        self.button_container.pack(expand=True, fill=tk.X)

        # Style for larger buttons
        style = ttk.Style()
        style.configure('Nav.TButton', font=('Arial', 12))
        
        # Navigation buttons
        self.controls_frame = ttk.Frame(self.button_container)
        self.controls_frame.pack(expand=True, pady=5)
        
        self.prev_button = ttk.Button(self.controls_frame, text="Previous", command=self.prev_page, 
                                      style='Nav.TButton', width=15)
        self.prev_button.pack(side=tk.LEFT, padx=5, pady=5)
        
        self.page_label = ttk.Label(self.controls_frame, text="Page: 0/0", font=('Arial', 12))
        self.page_label.pack(side=tk.LEFT, padx=10, pady=5)
        
        self.next_button = ttk.Button(self.controls_frame, text="Next", command=self.next_page, 
                                     style='Nav.TButton', width=15)
        self.next_button.pack(side=tk.LEFT, padx=5, pady=5)
        
        # No graphs initially
        self.canvas = None
        self.fig_canvas = None
        self.update_buttons()
    
    def draw_graph(self, vertices, edges, origin, destinations, title):
        """Modified draw_graph function that adds to the gallery instead of showing the plot"""
        # Create figure
        fig, ax = plt.subplots(figsize=(8, 8))

        # Set up Grid
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 10)
        ax.grid(True)
        ax.set_aspect('equal')
        
        # Draw vertices
        for name, (x, y) in vertices.items():
            if name == origin:
                color = 'limegreen'
            elif name in destinations:
                color = 'orange'
            else:
                color = 'skyblue'

            ax.plot(x, y, 'o', markersize=10, color=color)
            label = str(name)
            if name == origin:
                label += " (Origin)"
            elif name in destinations:
                label += " (Dest)"
            ax.text(x + 0.1, y + 0.1, label, fontsize=12, 
                   bbox=dict(facecolor='white', alpha=0.7, edgecolor='none'),
                   zorder=4)

        # Draw edges
        edge_set = set(edges.keys())
        drawn = set()
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
        
        # Store the figure
        self.graphs.append((fig, title))
        
        # Update display
        self.current_page = len(self.graphs) - 1
        self.display_current_graph()
        self.update_buttons()
        
        return fig
    
    def draw_solution(self, graph_map, origin, destinations, solution_path, title, metrics=None):

        # Create figure with side-by-side subplots - one for graph, one for table
        fig = plt.figure(figsize=(14, 8))

        # Adjust subplots ratio
        gs = gridspec.GridSpec(1, 2, width_ratios=[2, 1])
        
        # Create subplot for the graph (left side)
        ax_graph = fig.add_subplot(gs[0])
        
        # Set up Grid
        ax_graph.set_xlim(0, 10)
        ax_graph.set_ylim(0, 10)
        ax_graph.grid(True)
        ax_graph.set_aspect('equal')
        
        # Draw vertices
        vertices = graph_map.locations
        for name, (x, y) in vertices.items():
            if name == origin:
                color = 'limegreen'
            elif name in destinations:
                color = 'orange'
            else:
                color = 'skyblue'

            ax_graph.plot(x, y, 'o', markersize=10, color=color)
            label = str(name)
            if name == origin:
                label += " (Origin)"
            elif name in destinations:
                label += " (Dest)"
            ax_graph.text(x + 0.1, y + 0.1, label, fontsize=12, 
                bbox=dict(facecolor='white', alpha=0.7, edgecolor='none'),
                zorder=4)

        # Draw edges
        edges = {}
        for node1 in graph_map.graph_dict:
            for node2, cost in graph_map.graph_dict[node1].items():
                edges[(node1, node2)] = cost
        edge_set = set(edges.keys())
        drawn = set() # Track whether the edge has been drawn 
        for (src, dst) in edges.keys():
            x0, y0 = vertices[src]
            x1, y1 = vertices[dst]
            
            if (dst, src) in edge_set and (dst, src) not in drawn:
                # Undirected
                ax_graph.plot([x0, x1], [y0, y1], 'k-', lw=1.5)
                ax_graph.plot(x0, y0, 'o', markersize=5, color='black')
                ax_graph.plot(x1, y1, 'o', markersize=5, color='black')

            elif (dst, src) not in edge_set:
                # Directed
                ax_graph.annotate("",
                        xy=(x1, y1), xycoords='data',
                        xytext=(x0, y0), textcoords='data',
                        arrowprops=dict(arrowstyle="->", color='black', lw=1.5, mutation_scale=20))

            drawn.add((src, dst))

        # Draw Solution Path
        if solution_path and len(solution_path) > 1:
            for i in range(len(solution_path) - 1):
                src = solution_path[i]
                dst = solution_path[i + 1]
                
                x0, y0 = vertices[src]
                x1, y1 = vertices[dst]
                
                if (src, dst) in edges:
                    ax_graph.annotate("",
                                xy=(x1, y1), xycoords='data',
                                xytext=(x0, y0), textcoords='data',
                                arrowprops=dict(arrowstyle="->", color='red', lw=3, mutation_scale=20))
        
        ax_graph.set_title(title)
        
        # Create the metrics table (right side)
        ax_table = fig.add_subplot(gs[1])
        
        # Hide axes for table subplot
        ax_table.axis('off')
        
        # Create the table data
        if metrics is None:
            metrics = {}
        
        # Default metrics if not provided
        data = [
            ['Nodes Explored', metrics.get('nodes_explored', 'N/A')],
            ['Runtime (miliseconds)', f"{metrics.get('runtime', 'N/A'):.6f}" if isinstance(metrics.get('runtime'), (int, float)) else 'N/A'],
            ['Algorithm', metrics.get('algorithm', 'N/A')]
        ]
        
        # Create the table
        table = ax_table.table(
            cellText=data,
            cellLoc='center',
            loc='center',
            colWidths=[0.8, 0.3]
        )
        
        # Styling the table
        table.auto_set_font_size(False)
        table.set_fontsize(10)
        table.scale(1.2, 2)
        
        # Adjust spacing
        #plt.tight_layout()
        
        # Store the figure
        self.graphs.append((fig, title))
        
        # Update display
        self.current_page = len(self.graphs) - 1
        self.display_current_graph()
        self.update_buttons()
        
        return fig
    
    def display_current_graph(self):
        """Display the current graph page"""
        # Clear previous canvas if exists
        if self.canvas:
            self.canvas.get_tk_widget().destroy()
        
        if 0 <= self.current_page < len(self.graphs):
            fig, title = self.graphs[self.current_page]
            
            # Create canvas
            self.canvas = FigureCanvasTkAgg(fig, master=self.canvas_frame)
            self.canvas.draw()
            self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
            
            # Update page label
            self.page_label.config(text=f"Page: {self.current_page + 1}/{len(self.graphs)} - {title}")
    
    def next_page(self):
        """Navigate to next page"""
        if self.current_page < len(self.graphs) - 1:
            self.current_page += 1
            self.display_current_graph()
            self.update_buttons()
    
    def prev_page(self):
        """Navigate to previous page"""
        if self.current_page > 0:
            self.current_page -= 1
            self.display_current_graph()
            self.update_buttons()
    
    def update_buttons(self):
        """Update button states based on current page"""
        if len(self.graphs) == 0:
            self.prev_button.config(state=tk.DISABLED)
            self.next_button.config(state=tk.DISABLED)
            self.page_label.config(text="No graphs available")
        else:
            self.prev_button.config(state=tk.NORMAL if self.current_page > 0 else tk.DISABLED)
            self.next_button.config(state=tk.NORMAL if self.current_page < len(self.graphs) - 1 else tk.DISABLED)
    
    def on_closing(self):
        print("Window is closing...")
        self.root.destroy()
        sys.exit()
