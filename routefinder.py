from queue import PriorityQueue
from Graph import *
from math import sqrt

class map_state() :
    ## f = total estimated cost
    ## g = cost so far
    ## h = estimated cost to goal
    def __init__(self, location="", mars_graph=None,
                 prev_state=None, g=0,h=0):
        self.location = location
        self.mars_graph = mars_graph
        self.prev_state = prev_state
        self.g = g
        self.h = h
        self.f = self.g + self.h

    def __eq__(self, other):
        return self.location == other.location

    def __hash__(self):
        return hash(self.location)

    def __repr__(self):
        return "(%s)" % (self.location)

    def __lt__(self, other):
        return self.f < other.f

    def __le__(self, other):
        return self.f <= other.f

    def is_goal(self):
        return self.location == '1,1'
    
    def successors(self):
        successors_list = []
        for neighbor, cost in self.mars_graph.get_neighbors_and_costs(self.location):
            new_g = self.g + cost
            new_h = 0  
            new_state = map_state(location=neighbor, mars_graph=self.mars_graph, prev_state=self, g=new_g, h=new_h)
            successors_list.append(new_state)
        return successors_list
    
def a_star(start_state, heuristic_fn, goal_test, use_closed_list=True) :
    search_queue = PriorityQueue()
    closed_list = {}
    counter = 0

    search_queue.put((start_state.f, start_state))

    while not search_queue.empty():
        current_f, current_state = search_queue.get()

        if goal_test(current_state):
            print("Goal found")
            print(current_state)
            print(f"Number of states generated: {counter}")
            return current_state

        if use_closed_list:
            if current_state in closed_list and closed_list[current_state] < current_f:
                continue  
            closed_list[current_state] = current_f

        successors = current_state.successors() 
        for successor in successors:
            successor.h = heuristic_fn(successor)  
            successor.f = successor.g + successor.h


            if use_closed_list and (successor in closed_list and closed_list[successor] <= successor.g):
                continue  

            search_queue.put((successor.f, successor))
            counter += 1

    print(f"Number of states generated: {counter}")
    return None


## default heuristic - we can use this to implement uniform cost search
def h1(state) :
    return 0

## you do this - return the straight-line distance between the state and (1,1)
def sld(state) :
    x, y = map(int, state.location.split(','))  
    x1, y1 = 1, 1  
    distance = sqrt((x - x1) ** 2 + (y - y1) ** 2)
    return distance

## you implement this. Open the file filename, read in each line,
## construct a Graph object and assign it to self.mars_graph().
def read_mars_graph(filename):
    graph = Graph()
    with open(filename, 'r') as file:
        for line in file:
            parts = line.strip().split(':')
            node_str = parts[0].strip()
            neighbors_str = parts[1].strip().split(' ')
            
            if node_str not in graph.g:
                graph.add_node(node_str)
            
            for neighbor_str in neighbors_str:
                if neighbor_str:  
                    if neighbor_str not in graph.g:
                        graph.add_node(neighbor_str)
                    
                    edge = Edge(node_str, neighbor_str, 1)  
                    graph.add_edge(edge)
    return graph