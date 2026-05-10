from src.core.movement import DIRECTIONS

def generate_solution_steps(board, solution):
    steps = []
    current_x = board.start.x
    current_y = board.start.y
    last_checkpoint = -1

    steps.append((0,'Initial', (current_x, current_y), last_checkpoint))

    direction_map = {
        'U': 'UP',
        'D': 'DOWN',
        'L': 'LEFT',
        'R': 'RIGHT'
    }

    for step_index, move_char in enumerate(solution, start=1):
        direction = direction_map[move_char]
        dx, dy = DIRECTIONS[direction]

        while True:
            nx = current_x + dx
            ny = current_y + dy

            if not board.is_inside(nx, ny):
                break

            tile = board.get_tile(nx, ny)

            if tile == 'X':
                break

            if tile.isdigit():
                checkpoint_num = int(tile)
                if checkpoint_num == last_checkpoint + 1:
                    last_checkpoint = checkpoint_num

            current_x = nx
            current_y = ny

        steps.append((step_index, move_char, (current_x, current_y), last_checkpoint))

    return steps