import os
import time

class ExportService:
    @staticmethod
    def export_solution(board, result, steps, algorithm, heuristic=None):
        output_dir = 'output'
        os.makedirs(output_dir, exist_ok=True)

        timestamp = time.strftime('%Y%m%d_%H%M%S')
        algo_name = algorithm.replace('*', 'Star')
        filename = (f'solution_{algo_name}')
        if heuristic:
            filename += f'_{heuristic}'
        filename += f'_{timestamp}.txt'
        filepath = os.path.join(output_dir, filename)

        with open(filepath, 'w') as file:
            file.write('=' * 50 + '\n')
            file.write('Ice Sliding Puzzle Solver\n')
            file.write('=' * 50 + '\n\n')

            file.write(f'Algorithm : {algorithm}\n')
            if heuristic:
                file.write(f'Heuristic : {heuristic}\n')
            file.write(f'Solution  : {result["solution"]}\n')
            file.write(f'Cost      : {result["cost"]}\n')
            file.write(f'Iterations: {result["iterations"]}\n')
            file.write(f'Time      : {result["time_ms"]:.2f} ms\n\n' )

            file.write('=' * 50 + '\\n')
            file.write('PLAYBACK STATES\\n')
            file.write('=' * 50 + '\\n\\n')

            for step_index, move, pos, last_num in steps:
                if step_index == 0:
                    file.write('INITIAL STATE\\n')
                else:
                    file.write(f'STEP {step_index} : 'f'{move}\\n')

                for row in range(board.rows):
                    row_text = ''
                    for col in range(board.cols):
                        if (row, col) == pos:
                            row_text += 'Z'
                        else:
                            row_text += board.grid[row][col]

                    file.write(row_text + '\\n')

                file.write('\\n')

        return os.path.abspath(filepath)