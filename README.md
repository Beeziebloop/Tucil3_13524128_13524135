# Tucil3_13524128_13524135

# Ice Sliding Puzzle Solver

## Deskripsi Program

Ice Sliding Puzzle Solver adalah program berbasis Python yang digunakan untuk mencari solusi optimal pada permainan *Ice Sliding Puzzle* menggunakan algoritma pathfinding.

Pada permainan ini, pemain bergerak di atas papan es dan akan terus meluncur ke satu arah hingga menabrak dinding. Program mendukung beberapa algoritma pencarian, yaitu:
* Uniform Cost Search (UCS)
* Greedy Best First Search (GBFS)
* A* Search

Program juga menyediakan GUI menggunakan **Pygame** yang memungkinkan pengguna untuk:
* Memuat file puzzle `.txt`
* Memilih algoritma dan heuristic
* Menjalankan solver
* Melihat visualisasi solusi
* Melakukan playback langkah solusi
* Mengekspor hasil solusi ke file `.txt`

---

# Requirement Program

## Software

* Python 3.10 atau lebih baru

## Library Python

Dependency program terdapat pada file:

```text
requirements.txt
```

Isi:

```text
pygame==2.6.1
```

---

# Instalasi

Disarankan menggunakan virtual environment.

## Windows

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

## Linux / macOS

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

# Cara Menjalankan Program

Jalankan program dari root folder project:

```bash
python main.py
```

---

# Cara Menggunakan Program

1. Tekan tombol **LOAD MAP**
2. Pilih file input `.txt`
3. Pilih algoritma:

   * UCS
   * GBFS
   * A*
4. Pilih heuristic (untuk GBFS dan A*)
5. Tekan tombol **RUN SOLVER**
6. Program akan:

   * Menampilkan solusi
   * Menampilkan visualisasi board
   * Menampilkan statistik pencarian
   * Menyediakan playback solusi
   * Menyimpan hasil solusi ke file `.txt`

---

# Format Input

Program menerima file `.txt` yang merepresentasikan board puzzle.

Contoh:

```text
XXXXXXX
X0****X
X**X**X
X****OX
X1***LX
XS**X*X
XXXXXXX
```

Keterangan simbol:

| Simbol | Arti       |
| ------ | ---------- |
| `S`    | Start      |
| `O`    | Goal       |
| `X`    | Wall       |
| `L`    | Lava       |
| `0-9`  | Checkpoint |
| `*`    | Tile biasa |

---

# Output Program

Program menghasilkan:

* Solusi path
* Total cost
* Banyak iterasi/node
* Waktu eksekusi
* Playback visualisasi
* File output `.txt`

File output disimpan pada:

```text
test/output/
```

---

# Author

* Safira Berlianti (13524128)
* Varistha Devi (13524135)
