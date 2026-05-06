from src.core.state import State

DIRECTIONS = {
    "UP": (-1, 0),
    "DOWN": (1, 0),
    "LEFT": (0, -1),
    "RIGHT": (0, 1)
}

def slide(board, state, direction):
    dx, dy = DIRECTIONS[direction]
    x, y = state.x, state.y
    current_last_num = state.last_num
    total_movement_cost = 0

    while True:
        nx, ny = x + dx, y + dy

        # game over kalo keluar dari board
        if not board.is_inside(nx, ny):
            return None

        tile = board.get_tile(nx, ny)

        # game over kalo masuk ke lava
        if tile == 'L':
            return None

        # berhenti kalo nabrak batu
        if tile == 'X':
            break
        
        # kalo lewat angka
        if tile.isdigit():
            # validasi urutan
            if int(tile) == current_last_num + 1:
                current_last_num = int(tile)
            else:
                return None
            
        # update cost
        total_movement_cost += board.costs[nx][ny]

        # lanjut geser
        x, y = nx, ny

    return State(x, y, current_last_num), total_movement_cost

def get_neighbors(board, state):
    neighbors = []

    for d in DIRECTIONS:
        next_state = slide(board, state, d)

        if next_state == state:
            continue

        neighbors.append(next_state)

    return neighbors