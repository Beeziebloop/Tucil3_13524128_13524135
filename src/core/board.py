class Board:
    def __init__(self, grid, costs,start, goal, max_num):
        self.grid = grid
        self.costs = costs
        self.start = start
        self.goal = goal
        self.max_num = max_num
        self.rows = len(grid)
        self.cols = len(grid[0])

    def is_inside(self, x, y):
        return 0 <= x < self.rows and 0 <= y < self.cols

    def get_tile(self, x, y):
        return self.grid[x][y]
    
    def is_goal(self, state):
        return self.grid[state.x][state.y] == 'O' and state.last_num == self.max_num