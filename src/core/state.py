class State:
    def __init__(self, x, y, last_num = -1):
        self.x = x
        self.y = y
        self.last_num = last_num

    def __eq__(self, other):
        if not isinstance(other, State): return False
        return self.x == other.x and self.y == other.y and self.last_num == other.last_num

    def __hash__(self):
        return hash((self.x, self.y, self.last_num))

    def __repr__(self):
        return f"({self.x},{self.y},{self.last_num})"