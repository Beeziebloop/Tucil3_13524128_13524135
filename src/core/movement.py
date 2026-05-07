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
            elif int(tile) <= current_last_num: #angka udah pernah dilewatin jadinya aman
                pass
            else:
                return None
            
        # update cost
        total_movement_cost += board.costs[nx][ny]

        # lanjut geser
        x, y = nx, ny

    return State(x, y, current_last_num), total_movement_cost

def get_neighbors(board, state):
    neighbors = []

    for d, (dx, dy) in DIRECTIONS.items():
        result = slide(board, state, d)
        if result is None: #kalau masuk lava/keluar map/checkpoint salah
            continue
        nextS, moveCost = result
        if nextS.x == state.x and nextS.y == state.y: #cek apakah benar-benar bergerak dan bukan stuck in place
            continue
        neighbors.append((d, nextS, moveCost))

    return neighbors