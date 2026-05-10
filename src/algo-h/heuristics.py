import math

def getHeuristic(name):
    heuristics = {
        "H1" : remCheckpointsAndGoal,
        "H2" : manhattanToNextActiveTar,
        "H3" : euclideanToNextActiveTar,
    }
    return heuristics.get(name)

#total manhattan distance untuk semua checkpoint yang tersisa ditambah goal
def remCheckpointsAndGoal(state, board):
    totDist = 0
    currentPos = (state.x, state.y)
    #jarak ke next checkpoint
    for num in range(state.last_num + 1, board.max_num + 1):
        nextPos = board.checkpointPos[num]
        totDist += abs(currentPos[0] - nextPos[0]) + abs(currentPos[1] - nextPos[1])
        currentPos = nextPos #update position buat checkpoint berikutnya
    #jarak checkpoint terakhir ke goal
    totDist += abs(currentPos[0] - board.goalPos[0]) + abs(currentPos[1] - board.goalPos[1])
    return totDist

#ngitung manhattan distance ke target aktif (bisa checkpoint berikutnya atay goal)
def manhattanToNextActiveTar(state, board):
    nextNum = state.last_num + 1
    #kalo ada checkpoint yang masih belum keambil
    if nextNum <= board.max_num:
        targetX, targetY = board.checkpointPos[nextNum]
    else: #kalau udah keambil semua, change target to goal
        targetX, targetY = board.goalPos
    return abs(state.x - targetX) + abs(state.y - targetY)

#ngitung euclidean distance ke target aktif
def euclideanToNextActiveTar(state, board):
    nextNum = state.last_num + 1
    if nextNum <= board.max_num:
        targetX, targetY = board.checkpointPos[nextNum]
    else:
        targetX, targetY = board.goalPos
    return math.sqrt((state.x - targetX)**2 + (state.y - targetY)**2)