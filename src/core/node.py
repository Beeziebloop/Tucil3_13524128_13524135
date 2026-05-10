#search node, isinya state dan metadata buat pathfinding
class Node:
    def __init__(self, state, parent=None, move=None, cost=0, heuristic=0):
        self.state = state 
        self.parent = parent
        self.move = move
        self.cost = cost #cost cumulative dari start
        self.heuristic = heuristic #heuristic estimate ke goal

    @property
    def f_score(self): #untuk A*
        return self.cost + self.heuristic
    
    def __lt__(self, other): #buat ngecompare priority queue
        if self.f_score != other.f_score:
            return self.f_score < other.f_score
        return self.cost < other.cost
    
    def __repr__(self):
        return f"({self.state}, {self.cost}, {self.heuristic}, {self.move})"
    
    @staticmethod
    def reconstruct_path(node): #reconstruct dari goal node dengan ngikutin parent pointers
        path = []
        cur = node
        while cur.parent is not None:
            path.append(cur.move)
            cur = cur.parent
        path.reverse() #direverse karena dibangunnya backwards tadi
        return "".join(path)
    
    @staticmethod
    def reconstruct_states(node):
        states = []
        while node is not None:
            states.append(node.state)
            node = node.parent
        states.reverse()
        return states