import networkx as nx
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter.simpledialog import askinteger



class suguruInput:  
    def __init__(self, root, rows, cols):
        self.root = root
        try:
            img = tk.PhotoImage(file="Suguru.png")
            self.root.iconphoto(False, img)
        except (tk.TclError, FileNotFoundError):
            print("error loading icon file")
        self.root.title("Suguru Inputter")

        
        # Set grid size
        self.rows = rows
        self.cols = cols
        
        self.cell_size = 100
        self.entry_vars = [[tk.StringVar() for _ in range(self.cols)] for _ in range(self.rows)]
        self.entries = [[None for _ in range(self.cols)] for _ in range(self.rows)]
        self.rectangles = [[None for _ in range(self.cols)] for _ in range(self.rows)]
        self.colors = [
            "#98FF98", "#FFDAB9", "#E6E6FA", "#FF7F50", "#87CEEB", "#C8A2C8", "#FA8072", "#FFFFE0",
            "#00FFFF", "#F4A460", "#B0E0E6", "#FFB6C1", "#E0B0FF", "#40E0D0", "#F0FFF0", "#CCCCFF",
            "#DE5D83", "#6495ED", "#93C572", "#DA70D6"
        ]
        self.current_color_index = 0
        self.drawing = False
        self.cell_colors = [[None for _ in range(self.cols)] for _ in range(self.rows)]
        
        self.create_grid()
        self.create_submit_button()
        self.canvas.bind("<B1-Motion>", self.on_mouse_drag)
        self.canvas.bind("<ButtonPress-1>", self.start_drawing)
        self.canvas.bind("<ButtonRelease-1>", self.stop_drawing)

    def create_grid(self):
        self.canvas = tk.Canvas(self.root, width=self.cols * self.cell_size, height=self.rows * self.cell_size)
        self.canvas.grid(row=0, column=0, rowspan=self.rows, columnspan=self.cols)
        
        for i in range(self.rows):
            for j in range(self.cols):
                x1 = j * self.cell_size
                y1 = i * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size
                rect = self.canvas.create_rectangle(x1, y1, x2, y2, fill='white', outline='black')
                entry = tk.Entry(self.root, textvariable=self.entry_vars[i][j], width=5, justify='center', bd=0)
                self.canvas.create_window(x1 + self.cell_size / 2, y1 + self.cell_size / 2, window=entry)
                self.entries[i][j] = entry
                self.rectangles[i][j] = rect

    def create_submit_button(self):
        submit_button = tk.Button(self.root, text="Submit", command=self.submit_and_close, bd=0, bg="#4CAF50", fg="white")
        submit_button.grid(row=self.rows + 1, columnspan=self.cols, pady=10)

    def start_drawing(self, event):
        self.drawing = True
        self.current_color_index = (self.current_color_index + 1) % len(self.colors)
        self.current_color = self.colors[self.current_color_index]

    def stop_drawing(self, event):
        self.drawing = False

    def on_mouse_drag(self, event):
        if self.drawing:
            col = event.x // self.cell_size
            row = event.y // self.cell_size
            if 0 <= col < self.cols and 0 <= row < self.rows:
                entry = self.entries[row][col]
                rect = self.rectangles[row][col]
                self.canvas.itemconfig(rect, fill=self.current_color)
                current_color = self.cell_colors[row][col]
                if current_color != self.current_color:
                    self.cell_colors[row][col] = self.current_color
                    entry.config(bg=self.current_color)  # Update entry field background color

    def submit_and_close(self):
        self.root.destroy()

    def submit(self):
        grid_values = []
        for i in range(self.rows):
            row_values = []
            for j in range(self.cols):
                value = self.entry_vars[i][j].get()
                try:
                    value = int(value)
                except ValueError:
                    value = None
                row_values.append(value)
            grid_values.append(row_values)
        cell_colors = self.cell_colors
        return grid_values, cell_colors


def adjacentNodes(node, gridValues):
    x, y = pos[node]
    adjacentNodes = []
    for x_shift in range(-1, 2):
        for y_shift in range(-1, 2):
            if x_shift == 0 and y_shift == 0:
                continue
            new_x = x + x_shift
            new_y = y + y_shift
            if 0 <= new_x < len(gridValues) and 0 <= new_y < len(gridValues[0]):
                adjacentNodes += [key for key, value in pos.items() if value == (new_x, new_y)]
    return adjacentNodes

def regionNodes(node, regionValues):
    x, y = pos[node]
    regionValue = regionValues[x][y]
    regionNodes = []
    for i in range(len(regionValues)):
        for j in range(len(regionValues[0])):
            if i == x and j == y:
                continue
            if regionValues[i][j] == regionValue:
                regionNodes += [key for key, value in pos.items() if value == (i, j)]
    return regionNodes

def create_graph(gridValues, regionValues):
    global pos
    pos = {}
    values = {}
    initial_values = {}
    for i in range(len(gridValues)):
        for j in range(len(gridValues[0])):
            name = f"{i},{j}"
            values[name] = gridValues[i][j]
            if gridValues[i][j] is not None:
                displayName = str(gridValues[i][j])
                initial_values[name] = gridValues[i][j]
            else:
                displayName = ""
            G.add_node(name, label=displayName)
            pos[name] = (i, j)
    
    nx.set_node_attributes(G, values, 'values')
    nx.set_node_attributes(G, initial_values, 'initialValues')

    for node1 in G.nodes:
        for node2 in adjacentNodes(node1, gridValues):
            G.add_edge(node1, node2, label="adjacent")
        for node2 in regionNodes(node1, regionValues):
            G.add_edge(node1, node2, label="region")

def display_graph(pos, **kwargs):
    color_map = {'adjacent': 'blue', 'region': 'pink'}
    
    labels_with_possible_values = {}
    font_color = {}
    font_size = {}

    existing_labels = nx.get_node_attributes(G, 'label')
    possible_values = nx.get_node_attributes(G, 'possibleValues')
    initial_values = nx.get_node_attributes(G, 'initialValues')

    for node in G.nodes:
        if node in possible_values and len(possible_values[node]) >= 1 and kwargs.get('showPossibleValues', True):
            labels_with_possible_values[node] = ','.join(map(str, possible_values[node]))
            font_color[node] = 'red'
            font_size[node] = 8
        elif node in initial_values:
            labels_with_possible_values[node] = existing_labels.get(node, "")
            font_color[node] = 'purple'
            font_size[node] = 12
        else:
            labels_with_possible_values[node] = existing_labels.get(node, "")
            font_color[node] = 'black'
            font_size[node] = 12

    plt.figure()
        

    display_pos = {node: (y, -x) for node, (x, y) in pos.items()}

    if 'graphTitle' in kwargs:
        plt.title(kwargs.get('graphTitle'))

    padding_factor = 0.05
    pos_with_padding = {node: (x * (1 - padding_factor), y * (1 - padding_factor)) for node, (x, y) in display_pos.items()}
    
    nx.draw_networkx_nodes(G, pos=pos_with_padding, node_size=1000, node_color='white', edgecolors='black', node_shape='s')
    nx.draw_networkx_edges(G, pos=pos_with_padding, edge_color=[color_map[G[u][v]['label']] for u, v in G.edges()])
    
    for node, (x, y) in pos_with_padding.items():
        nx.draw_networkx_labels(G, {node: (x, y)}, labels={node: labels_with_possible_values[node]}, font_size=font_size[node], font_color=font_color[node])
    
    plt.axis('off')
    plt.show()

def setup_graph(gridValues, regionValues):
    global G
    G = nx.Graph()
    create_graph(gridValues, regionValues)

def graph_region_nodes(node):
    region_nodes = []
    for neighbour in G.neighbors(node):
        if G.edges[node, neighbour]['label'] == 'region':
            region_nodes.append(neighbour)
    return region_nodes

def graph_adjacent_nodes(node):
    adjacent_nodes = []
    for neighbour in G.neighbors(node):
        if G.edges[node, neighbour]['label'] == 'adjacent':
            adjacent_nodes.append(neighbour)
    return adjacent_nodes

def updateValue(node, value):
    values = nx.get_node_attributes(G, 'values')
    values[node] = value
    nx.set_node_attributes(G, values, 'values')
    
    labels = nx.get_node_attributes(G, 'label')
    labels[node] = str(value)
    nx.set_node_attributes(G, labels, 'label')
    
    possibleValues = nx.get_node_attributes(G, 'possibleValues')
    if node in possibleValues:
        possibleValues[node] = []
    else:
        print(f"No possible values to remove for node {node}")
    nx.set_node_attributes(G, possibleValues, 'possibleValues')
    nx.set_node_attributes(G, values, 'values')

def numNotNone(dictionary):
    count = 0
    for value in dictionary.values():
        if value is not None:
            count += 1
    return count

def sharedNeighbours(nodeList):
    neighbor_count = {}
    shared_neighbours = []

    # Count occurrences of each adjacent node
    for node in nodeList:
        adj_nodes = graph_adjacent_nodes(node)
        for adj_node in adj_nodes:
            if adj_node not in nodeList:  # Ignore nodes in nodeList
                if adj_node not in neighbor_count:
                    neighbor_count[adj_node] = 0
                neighbor_count[adj_node] += 1

    # Identify shared neighbors
    for node, count in neighbor_count.items():
        if count == len(nodeList):
            shared_neighbours.append(node)

    return shared_neighbours


def initPossibleValues(node):
    region_size = len(graph_region_nodes(node)) + 1
    node_possible_values = [i for i in range(1, region_size + 1)]

    possible_values = nx.get_node_attributes(G, 'possibleValues')
    values = nx.get_node_attributes(G, 'values')

    # Eliminate values based on region constraints
    for region_node in graph_region_nodes(node):
        if values.get(region_node) is not None:
            if values[region_node] in node_possible_values:
                node_possible_values.remove(values[region_node])

    # Eliminate values based on adjacent constraints
    for adjacent_node in graph_adjacent_nodes(node):
        if values.get(adjacent_node) is not None and values[adjacent_node] in node_possible_values:
            node_possible_values.remove(values[adjacent_node])

    possible_values[node] = node_possible_values
    nx.set_node_attributes(G, possible_values, 'possibleValues')
    #print(f"Updated possible values for node {node}: {possible_values[node]}")


def updatePossibleValues(node):
    # Retrieve current possible values and node values from the graph
    current_possible_values = nx.get_node_attributes(G, 'possibleValues')[node]
    values = nx.get_node_attributes(G, 'values')
    
    # Debugging statements to track the updates
    #print(f"Updating possible values for node {node}: {current_possible_values}")
    
    # Update based on region nodes
    for region_node in graph_region_nodes(node):
        if values[region_node] is not None and values[region_node] in current_possible_values:
            current_possible_values.remove(values[region_node])
            #print(f"Removed value {values[region_node]} from possible values of {node} due to region constraint")
    
    # Update based on adjacent nodes
    for adjacent_node in graph_adjacent_nodes(node):
        if values[adjacent_node] is not None and values[adjacent_node] in current_possible_values:
            current_possible_values.remove(values[adjacent_node])
            #print(f"Removed value {values[adjacent_node]} from possible values of {node} due to adjacent constraint")
    
    # Update the graph with the new possible values
    nx.set_node_attributes(G, {node: current_possible_values}, 'possibleValues')
    #print(f"Updated possible values for node {node}: {current_possible_values}")





def lastInRegion(node):
    possibleValues = nx.get_node_attributes(G, 'possibleValues')
    region_nodes = graph_region_nodes(node)

    for possibleValue in possibleValues.get(node, []):
        is_unique = True
        for region_node in region_nodes:
            if possibleValue in possibleValues.get(region_node, []):
                is_unique = False
                break
        if is_unique:
            return possibleValue
    return None

def nodeSolvable(node):
    possibleValues = nx.get_node_attributes(G, 'possibleValues')
    if len(possibleValues[node]) == 1:
        return possibleValues[node][0]
    last_value = lastInRegion(node)
    if last_value is not None:
        return last_value
    return None


def updateStack(stack, node):
    values = nx.get_node_attributes(G, 'values')
    for region_node in graph_region_nodes(node):
        if values.get(region_node) is None and region_node not in stack:
            stack.append(region_node)
    for adjacent_node in graph_adjacent_nodes(node):
        if values.get(adjacent_node) is None and adjacent_node not in stack:
            stack.append(adjacent_node)
    return stack


def suguruSolver():
    show_steps = True
    show_minor_steps = True
    possible_values = {}
    nx.set_node_attributes(G, possible_values, 'possibleValues')

    # Initialize possible values for all empty nodes
    for node in G.nodes:
        if G.nodes[node]['values'] is None:
            initPossibleValues(node)

    display_graph(pos, showPossibleValues=True, graphTitle="Initialization phase complete")

    innerLoop = True
    update_made = True
    iteration_count = 0
    nodes_solved = 0
    suguru_solved = False

    while update_made:
        update_made = False
        possibleValues = nx.get_node_attributes(G, 'possibleValues')
        #print(f"start of the majorLoop: {possibleValues}")

        # Basic checking at the start of the loop
        values = nx.get_node_attributes(G, 'values')
        if numNotNone(values) == len(G.nodes):
            print("Solution found")
            display_graph(pos, showPossibleValues=False, graphTitle="Solved state")
            suguru_solved = True
            break

        if iteration_count != 0:
            display_graph(pos, showPossibleValues=True, graphTitle=f"Iteration: {iteration_count}")
        iteration_count += 1
        
        # Inner loop no. 1
        print("starting innerLoop1\n")
        while innerLoop:
            values = nx.get_node_attributes(G, 'values')
            innerLoop = False
            for node in G.nodes:
                #print(f"innerLoop1, current node: {node}, with values: {values.get(node)}")
                
                # Check if the node is solvable
                if values.get(node) is None:
                    updatePossibleValues(node)
                    possibleValues = nx.get_node_attributes(G, 'possibleValues')

                    stack = []
                    solvable_value = nodeSolvable(node)
                    if solvable_value is not None:
                        updateValue(node, solvable_value)
                        print(f"SOLVED NODE: {node} to value: {solvable_value}")
                        stack = updateStack(stack, node)
                        innerLoop = True
                        nodes_solved += 1
                        update_made = True

                    while stack:
                        #print(f"stack: {stack}")
                        node = stack.pop()
                        updatePossibleValues(node)
                        possibleValues = nx.get_node_attributes(G, 'possibleValues')
                        #print(f"node: {node}, with possible values: {possibleValues[node]}")
                        solvable_value = nodeSolvable(node)
                        if solvable_value != None:
                            print(f"SOLVED NODE: {node} with value: {solvable_value}")
                            updateValue(node, solvable_value)
                            stack = updateStack(stack, node)
                            innerLoop = True
                            nodes_solved += 1
                            update_made = True

        # Inner loop no. 2
        print(f"on iteration: {iteration_count}, nodes solved: {nodes_solved}, starting innerLoop2")
        breaker = False
        values = nx.get_node_attributes(G, 'values')
        possibleValues = nx.get_node_attributes(G, 'possibleValues')
        #print(f"Possible values before innerLoop2: {possibleValues}")

        #chaning algo to go thru each region instead
        visited_nodes = []
        for node in G.nodes:
            if node in visited_nodes:
                continue
            else:
                visited_nodes.append(node)
                for reg_node in graph_region_nodes(node):   #add all region nodes to the visited nodes so it goes through one region at a time
                    visited_nodes.append(reg_node)
            #print(f"sharing neighbours; testing: {node}")
            for posVal in range(1, len(graph_region_nodes(node)) + 2):
                #print(f"     testing posVal: {posVal}")
                #get a list of nodes that contain the same posVal within the current region
                possible_region_nodes = []
                if values[node] == None and posVal in possibleValues[node]:
                    possible_region_nodes.append(node)
                for region_node in graph_region_nodes(node):
                    #print(f"testing: {region_node}, with value: {values[node]} and possibleValues: {possibleValues.get(node, [])}")
                    if values[region_node] == None and posVal in possibleValues[region_node]:
                        possible_region_nodes.append(region_node)
                #print(f"possible_region_nodes: {possible_region_nodes}")
                
                #get the shared neighbour(s) of these nodes (then filter down possibilites)
                shared_neighbours_opts = sharedNeighbours(possible_region_nodes)
                shared_neighbours = []
                for opt in shared_neighbours_opts:
                    if values[opt] is None and posVal in possibleValues[opt]:
                        shared_neighbours.append(opt)
                #print(f"filtered shared neighbours: {shared_neighbours}")
                
                #if there are shared neighbour(s) then remove the posVal from that/ those shared neighbour(s)
                for shared_neighbour in shared_neighbours:
                    if posVal in possibleValues[shared_neighbour]:
                        print(f"removing {posVal} from {possibleValues[shared_neighbour]} in {shared_neighbour}")
                        possibleValues[shared_neighbour].remove(posVal)
                        if not possibleValues[shared_neighbour]:
                            print(f"Error: Node {shared_neighbour} has no possible values left after removal.")
                            return  # or raise an exception / handle error appropriately
                        innerLoop, breaker, update_made = True, True, True
                        nx.set_node_attributes(G, possibleValues, 'possibleValues')

            if breaker:
                break
        possibleValues = nx.get_node_attributes(G, 'possibleValues')      

    if not suguru_solved:
        print("No solution found")
        display_graph(pos, showPossibleValues=False, graphTitle="No solution found")




def hardcoded_input(rows, cols):

    # Provide a hardcoded example for a given grid size
    if rows == 5 and cols == 5:
        gridValues = [[5, None, None, 1, None, None, 2, None], [None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, 4], [None, None, None, None, None, None, None, 2], [None, None, None, None, 2, 5, None, None], [1, None, 2, None, None, None, None, None], [None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None]]

        regionValues = [['#E6E6FA', '#E6E6FA', '#E6E6FA', '#FF7F50', '#FF7F50', '#FF7F50', '#87CEEB', '#87CEEB'], ['#FFDAB9', '#E6E6FA', '#E6E6FA', '#FF7F50', '#FF7F50', '#C8A2C8', '#87CEEB', '#87CEEB'], ['#FFDAB9', '#FA8072', '#FFFFE0', '#FFFFE0', '#C8A2C8', '#C8A2C8', '#C8A2C8', '#87CEEB'], ['#FA8072', '#FA8072', '#FA8072', '#FFFFE0', '#FFFFE0', '#C8A2C8', '#CCCCFF', '#CCCCFF'], ['#00FFFF', '#FA8072', '#F4A460', '#FFFFE0', '#E0B0FF', '#CCCCFF', '#CCCCFF', '#CCCCFF'], ['#00FFFF', '#00FFFF', '#F4A460', '#E0B0FF', '#E0B0FF', '#E0B0FF', '#F0FFF0', '#F0FFF0'], ['#00FFFF', '#00FFFF', '#F4A460', '#F4A460', '#E0B0FF', '#FFB6C1', '#F0FFF0', '#F0FFF0'], ['#B0E0E6', '#B0E0E6', '#B0E0E6', '#F4A460', '#FFB6C1', '#FFB6C1', '#40E0D0', '#40E0D0']]
    else:
        # Initialize empty grid values and random colors for regions for larger sizes
        gridValues = [[None for _ in range(cols)] for _ in range(rows)]
        regionValues = [['#%02X%02X%02X' % (i * 10, j * 10, (i + j) * 10) for j in range(cols)] for i in range(rows)]
    return gridValues, regionValues

if __name__ == "__main__":
    use_gui = True  # Set to False to use hardcoded input

    if use_gui:
        root = tk.Tk()
        rows = askinteger("Input", "Enter number of rows:", minvalue=1, maxvalue=20)
        cols = askinteger("Input", "Enter number of columns:", minvalue=1, maxvalue=20)
        if not rows:
            rows = 5
        if not cols:
            cols = 5
        app = suguruInput(root, rows, cols)
        root.mainloop()
        gridValues, regionValues = app.submit()
        print(gridValues, regionValues)
    else:
        rows = 5  # or any other size for hardcoded input
        cols = 5  # or any other size for hardcoded input
        gridValues, regionValues = hardcoded_input(rows, cols)

    setup_graph(gridValues, regionValues)
    display_graph(pos, showPossibleValues=False, graphTitle="Initial state")
    suguruSolver()





"""
WHEN TRACING WHAT IS HAPPENING NOTICED TWO THINGS:
1. The stack should've continued - likely cuz stack priorisation needs reworking
2. there was a double-up made, as in two adjcanet cells were given the same value - likely cuz the possible vals weren't updated correctly

PROBLEM:
VALUES NEED TO BE UPDATED, BEFORE AND SO THAT THE UPDATE POSSIBLE VALUES IS ACCURATE



NOW GO THROUGH:
- TRACE WHAT THE STACK IS DOING
- (NEED TO FIX UPDATEPOSSIBLEVALUES FUNCTION AS IT AINT WORKING PROPERLY)
"""
