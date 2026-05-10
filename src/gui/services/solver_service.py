import time
from src.algo_and_heu.UCS import ucs
from src.algo_and_heu.GBFS import gbfs
from src.algo_and_heu.AStar import aStar
from src.algo_and_heu.heuristics import getHeuristic


class SolverService:
    @staticmethod
    def run(board, algorithm, heuristic_name=None):
        algorithm = algorithm.upper()
        heuristic_func = None

        if algorithm in ['GBFS', 'A*']:
            heuristic_func = getHeuristic(heuristic_name.upper())
            if heuristic_func is None:
                raise ValueError(f'Invalid heuristic: {heuristic_name}')

        start_time = time.perf_counter()

        if algorithm == 'UCS':
            result = ucs(board)
        elif algorithm == 'GBFS':
            result = gbfs(board, heuristic_func)
        elif algorithm == 'A*':
            result = aStar(board, heuristic_func)
        else:
            raise ValueError(f'Invalid algorithm: {algorithm}')

        end_time = time.perf_counter()
        execution_ms = (end_time - start_time) * 1000
        result['time_ms'] = execution_ms
        return result