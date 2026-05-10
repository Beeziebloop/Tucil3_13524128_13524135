from heapq import heappush, heappop
from src.core.state import State
from src.core.node import Node, reconstruct_path
from src.core.movement import get_neighbors

def ucs(board):
    #init starting state dan node
    startState = State(x=board.start.x, y=board.start.y, last_num=-1)
    startNode = Node(state=startState, parent=None, move=None, cost=0)
    #menggunakan priority queue yang menyimpan (cost, node). karena menggunakan heapq, cost paling rendah akan dipop lebih dahulu
    frontier = []
    heappush(frontier, (0, startNode))
    visited = set()
    #track best cost untuk mencapai tiap state (buat update frontier)
    costSoFar = {startState:0}
    iterations = 0
    while frontier:
        #pop state dengan cost terendah
        currentCost, currentNode = heappop(frontier)
        iterations += 1
        #skip kalo udah visited
        if currentNode.state in visited: continue
        #kalau nggak, tandain visited
        visited.add(currentNode.state)
        #check goal, apakah udah sampe 'O' dan melewati semua checkpoint jika ada
        if board.is_goal(currentNode.state):
            return{'solution': reconstruct_path(currentNode), 'cost': currentNode.cost, 'iterations': iterations, 'found': True}
        #expand neighbors, coba keempat arah
        neighbors = get_neighbors(board, currentNode.state)
        for dirChar, nextState, moveCost in neighbors:
            #hitung cost kumulatif untuk reach next state
            newCost = currentNode.cost + moveCost
            #skip kalau udah visited
            if nextState in visited: continue
            #hanya add kalau kita nemuin path yang lebih murah
            if nextState not in costSoFar or newCost < costSoFar[nextState]:
                costSoFar[nextState] = newCost
                #bikin node baru
                newNode = Node(state=nextState, parent=currentNode, move=dirChar, cost=newCost)
            heappush(frontier, (newCost, newNode))
    #kalau frontier habis tanpa menemukan goal, berarti nggak ada solusi
    return {'solution': None, 'cost': 0, 'iterations': iterations, 'found': False}