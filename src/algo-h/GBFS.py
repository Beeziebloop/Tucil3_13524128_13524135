from heapq import heappush, heappop
from src.core.state import State
from src.core.node import Node, reconstruct_path
from src.core.movement import get_neighbors

def gbfs(board, heuristics):
    #init starting state dan node
    startState = State(board.start.x, board.start.y, last_num=-1)
    heuVal = heuristics(startState, board)
    startNode = Node(state=startState, parent=None, move=None, cost=0, heuristic=heuVal)
    #priority queue yang menyimpan (heuristic_value, node)
    frontier = []
    frontier_set = set()
    heappush(frontier, (heuVal, startNode))
    frontier_set.add(startState)
    visited = set()
    iters = 0
    while frontier:
        #pop node dengan heuristic value terendah
        heuVal, curNode = heappop(frontier)
        iters += 1
        frontier_set.discard(curNode.state)
        if curNode.state in visited: continue
        #mark visited
        visited.add(curNode.state)
        #goal test 
        if board.is_goal(curNode.state):
            return {'solution': reconstruct_path(curNode), 'cost': curNode.cost, 'iterations': iters, 'found': True}
        #expand neighbors
        neighbors = get_neighbors(board, curNode.state)
        for dirChar, nextState, moveCost in neighbors:
            if nextState in visited or nextState in frontier_set: continue
            #hitung cost aktual untuk tracking
            newCost = curNode.cost + moveCost
            #hitung heuristic untuk next state
            heuVal = heuristics(nextState, board)
            newNode = Node(state=nextState, parent = curNode, move=dirChar, cost=newCost, heuristic=heuVal)
            heappush(frontier, (heuVal, newNode))
            frontier_set.add(nextState)
    return {'solution': None, 'cost': 0, 'iterations': iters, 'found': False}