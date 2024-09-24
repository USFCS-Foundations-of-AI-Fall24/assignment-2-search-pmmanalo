from collections import deque
from Graph import *
from queue import PriorityQueue
from routefinder import *
import math

## We will append tuples (state, "action") in the search queue
def breadth_first_search(startState, action_list, goal_test, use_closed_list=True):
    search_queue = deque()
    closed_list = {}
    counter = 0  

    search_queue.append((startState, ""))
    if use_closed_list:
        closed_list[startState] = True
    
    while len(search_queue) > 0:
        next_state = search_queue.popleft()
        if goal_test(next_state[0]):
            print("Goal found")
            print(next_state)
            ptr = next_state[0]
            while ptr is not None:
                ptr = ptr.prev
                print(ptr)
            print("Total number of states generated:", counter)
            return next_state
        else:
            successors = next_state[0].successors(action_list)
            if use_closed_list:
                filtered_successors = [item for item in successors if item[0] not in closed_list]
                for s in filtered_successors:
                    closed_list[s[0]] = True
                successors = filtered_successors
            
            counter += len(successors)
            search_queue.extend(successors)

    print("Total number of states generated:", counter)
    return None  

def depth_first_search(startState, action_list, goal_test, use_closed_list=True, limit=None):
    search_queue = deque()
    closed_list = {}
    counter = 0  

    initial_depth = 0 if limit is not None else None
    search_queue.append((startState, "", initial_depth)) 
    if use_closed_list:
        closed_list[startState] = True

    while len(search_queue) > 0 :
        next_state, action, depth = search_queue.pop() if limit is not None else search_queue.pop()[:2] + (None,)
        
        if goal_test(next_state):
            print("Goal found")
            print(next_state)
            print(f"Number of states generated: {counter}")
            return next_state

        if limit is not None and depth >= limit:
            continue

        successors = next_state.successors(action_list)
        if use_closed_list:
            successors = [item for item in successors
                           if item[0] not in closed_list]
            for s in successors:
                closed_list[s[0]] = True

        for s in successors:
            counter += 1  
            new_depth = depth + 1 if depth is not None else None
            search_queue.append((s[0], s[1], new_depth))

    print(f"Number of states generated: {counter}")
    print("Goal not found within depth limit" if limit is not None else "Goal not found")
    return None

def iterative_deepening_search(startState, action_list, goal_test, use_closed_list=True):
    depth = 0
    while True:
        result = depth_first_search(startState, action_list, goal_test, use_closed_list, limit=depth)
        if result is not None:
            return result, depth  
        depth += 1   
    
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