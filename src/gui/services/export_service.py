import os
import time


class ExportService:

    @staticmethod
    def export_solution(
        board,
        result,
        steps,
        algorithm,
        heuristic=None
    ):

        # simpan ke test/output
        BASE_DIR = os.path.abspath(
            os.path.join(
                os.path.dirname(__file__),
                '../../../'
            )
        )
        output_dir = os.path.join(BASE_DIR, 'test', 'output')

        os.makedirs(output_dir, exist_ok=True)

        timestamp = time.strftime('%Y%m%d_%H%M%S')
        algo_name = algorithm.replace('*', 'Star')
        filename = f'solution_{algo_name}'
        if heuristic:
            filename += f'_{heuristic}'
        filename += f'_{timestamp}.txt'

        filepath = os.path.join(
            output_dir,
            filename
        )

        with open(filepath, 'w') as file:
            # HEADER
            file.write('=' * 45 + '\n')
            file.write('Ice Sliding Puzzle Solution\n')
            file.write('=' * 45 + '\n\n')

            file.write(
                f'Solution Path: '
                f'{result["solution"]}\n'
            )

            file.write(
                f'Total Cost: '
                f'{result["cost"]}\n'
            )

            file.write(
                f'Iterations: '
                f'{result["iterations"]}\n'
            )

            file.write(
                f'Execution Time: '
                f'{result["time_ms"]:.2f} ms\n'
            )

            file.write('\n')

            # STEP SECTION
            file.write('=' * 45 + '\n')
            file.write('Step-by-step Solution\n')
            file.write('=' * 45 + '\n\n')

            for step_index, move, pos, last_num in steps:
                # title step
                if step_index == 0:
                    file.write('Initial State:\n')
                else:
                    file.write(
                        f'Step {step_index}: '
                        f'{move}\n'
                    )

                # gambar board
                for row in range(board.rows):
                    row_text = ''
                    for col in range(board.cols):
                        if (row, col) == pos:
                            row_text += 'Z'

                        else:
                            row_text += (board.grid[row][col])

                    file.write(row_text + '\n')

                file.write('\n')

            # FOOTER
            file.write('=' * 45 + '\n')
            file.write('End of Solution\n')
            file.write('=' * 45 + '\n')

        return os.path.abspath(filepath)