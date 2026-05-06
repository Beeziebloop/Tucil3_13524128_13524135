from src.core.board import Board
from src.core.state import State

def parse_file(filepath):
    grid = []
    costs = []
    start = None
    goal = None
    numbers = []

    with open(filepath, 'r') as f:
        # baca N dan M
        line = f.readline().strip()
        if not line:
            raise ValueError("File kosong")
        
        try:
            n, m = map(int, line.split())
        except ValueError:
            raise ValueError("Baris pertama harus berisi dua angka (N M)")

        # baca grid map
        for i in range(n):
            row_str = f.readline().strip()

            if len(row_str) != m:
                raise ValueError(f"Baris map ke-{i+1} panjangnya {len(row_str)}, harusnya {m}")

            row_list = list(row_str) 
            grid.append(row_list)

            for j, cell in enumerate(row_list):
                if cell == 'Z':
                    start = State(i, j)
                elif cell == 'O':
                    goal = State(i, j)
                elif cell.isdigit():
                    if int(cell) < 0 or int(cell) > 9:
                        raise ValueError(f"Angka harus antara 0-9: {cell}")
                    else:
                        numbers.append(int(cell))
                elif cell not in ['X', 'L', '*']:
                    raise ValueError(f"Karakter tidak valid di grid: {cell}")
        
        # validasi urutan angka
        if numbers:
            numbers.sort()
            for idx, num in enumerate(numbers):
                if num != idx:
                    raise ValueError(f"Angka harus berurutan dari 0")
            max_num = numbers[-1]
        else:
            max_num = -1

        # baca costs
        for i in range(n):
            cost_line = f.readline().strip()
            if not cost_line:
                raise ValueError(f"Baris cost ke-{i+1} tidak ditemukan (harus ada {n} baris)")
            
            cost_row = list(map(int, cost_line.split()))
            if len(cost_row) != m:
                raise ValueError(f"Baris cost ke-{i+1} punya {len(cost_row)} kolom, harusnya {m}")
            
            costs.append(cost_row)

    if start is None or goal is None:
        raise ValueError("Map harus punya Start (Z) dan Goal (O)")

    return Board(grid, costs, start, goal, max_num)