from heapq import heappush, heappop
from src.core.state import State
from src.core.node import Node
from src.core.movement import get_neighbors


def aStar(board, heuristic):
    # init state dan node
    startState = State(board.start.x, board.start.y, last_num=-1)
    startNode = Node(state=startState, parent=None, move=None, cost=0, heuristic=heuristic(startState, board))

    # priority queue
    pq = []
    heappush(pq, (startNode.f_score, startNode))

    # nyimpen min cost utk tiap state
    visited = {}
    visited[startState] = 0

    iters = 0

    while pq:
        # pop node yg f nya paling kecil
        _, curNode = heappop(pq)
        curState = curNode.state

        iters += 1

        if curNode.cost > visited[curState]:
            continue
        # cek goal
        if board.is_goal(curState):
            return {'solution': Node.reconstruct_path(curNode), 'cost': curNode.cost, 'iterations': iters, 'found': True}

        # expand neighbors
        neighbors = get_neighbors(board, curState)

        for dirChar, nextState, moveCost in neighbors:
            newCost = curNode.cost + moveCost
            # skip kalo udh ada path yg lebih bagus
            if nextState in visited and newCost >= visited[nextState]:
                continue

            # update visited dan pq
            visited[nextState] = newCost
            newNode = Node(state=nextState, parent=curNode, move=dirChar, cost=newCost, heuristic=heuristic(nextState, board))
            heappush(pq, (newNode.f_score, newNode))

    return {'solution': None, 'cost': 0, 'iterations': iters, 'found': False}