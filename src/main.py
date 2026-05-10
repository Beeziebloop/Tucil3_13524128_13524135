import os
import sys
import time
from src.parser.parser import parse_file
from src.algo_and_heu.UCS import ucs
from src.algo_and_heu.GBFS import gbfs
from src.algo_and_heu.heuristics import getHeuristic
from src.core.movement import DIRECTIONS

try:
    if os.name == 'nt': #windows
        import msvcrt
    else: #unix/linux/mac
        import tty
        import termios
except ImportError:
    pass

def clearScreen():
    os.system('cls' if os.name == 'nt' else 'clear')

def displayBoard(board, playerPos):
    print()
    for i in range(board.rows):
        rowStr = ""
        for j in range(board.cols):
            if(i, j) == playerPos:
                rowStr += "Z" #player pos
            else:
                rowStr += board.grid[i][j]
        print(rowStr)
    print()

def getSolutionSteps(board, solution):
    steps = []
    currentX, currentY = board.start.x, board.start.y
    #initial state
    steps.append((0, "Initial", (currentX, currentY)))
    #simulasi tiap move
    for numStep, dirChar in enumerate(solution, start=1):
        #map char ke nama direction full
        directionMap = {'U': 'UP', 'D': 'DOWN', 'L': 'LEFT', 'R': 'RIGHT'}
        dir = directionMap[dirChar]
        dx, dy = DIRECTIONS[dir]
        #slide sampai berhenti
        while True:
            nx, ny = currentX + dx, currentY + dy
            if not board.is_inside(nx, ny): break
            tile = board.get_tile(nx, ny)
            if tile == 'X': break
            currentX, currentY = nx, ny
        steps.append((numStep, dirChar, (currentX, currentY)))
    return steps

def playback(board, steps):
    curStep = 0
    maxStep = len(steps)-1
    def displayCurStep():
        clearScreen()
        stepNum, dir, pos = steps[curStep]
        if stepNum == 0:
            print("="*45)
            print("Initial State")
            print("="*45)
        else:
            print("="*45)
            print(f"Step {stepNum}: {dir}")
            print("="*45)
        displayBoard(board, pos)
        print("="*45)
        print(f"Step {curStep}/{maxStep}")
        print("\nControls:")
        print("right arrow: next step")
        print("left arrow: previous step")
        print("Q: quit playback")
        print("ESC: jump to specific step")
        print("="*45)
    displayCurStep()
    # Platform-specific keyboard handling
    if os.name == 'nt':  #windows
        while True:
            if msvcrt.kbhit():
                key = msvcrt.getch()
                if key == b'\xe0':  #arrow key prefix
                    key = msvcrt.getch()
                    if key == b'K':  #left arrow
                        if curStep > 0:
                            curStep -= 1
                            displayCurStep()
                    elif key == b'M':  # Right arrow
                        if curStep < maxStep:
                            curStep += 1
                            displayCurStep()
                elif key == b'\x1b':  #ESC
                    print("\n>> Pada step berapa anda ingin melakukan playback :")
                    try:
                        jump_to = int(input().strip())
                        if 0 <= jump_to <= maxStep:
                            curStep = jump_to
                            displayCurStep()
                        else:
                            print(f"Step harus berada di antara 0 dan {maxStep}")
                            time.sleep(1)
                            displayCurStep()
                    except ValueError:
                        print("Invalid input")
                        time.sleep(1)
                        displayCurStep()
                elif key.lower() == b'q':  #Quit
                    break
    else:  #unix/linux/mac
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            while True:
                key = sys.stdin.read(1)
                if key == '\x1b':  #escape sequence
                    next_key = sys.stdin.read(1)
                    if next_key == '[':
                        arrow = sys.stdin.read(1)
                        if arrow == 'D':  #left arrow
                            if curStep > 0:
                                curStep -= 1
                                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
                                displayCurStep()
                                tty.setraw(sys.stdin.fileno())
                        elif arrow == 'C':  #right arrow
                            if curStep < maxStep:
                                curStep += 1
                                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
                                displayCurStep()
                                tty.setraw(sys.stdin.fileno())
                    else:
                        #ESC key alone
                        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
                        print("\n>> Pada step berapa anda ingin melakukan playback :")
                        try:
                            jump_to = int(input().strip())
                            if 0 <= jump_to <= maxStep:
                                curStep = jump_to
                                displayCurStep()
                            else:
                                print(f"Step harus berada di antara 0 dan {maxStep}")
                                time.sleep(1)
                                displayCurStep()
                        except ValueError:
                            print("Invalid input")
                            time.sleep(1)
                            displayCurStep()
                        tty.setraw(sys.stdin.fileno())
                elif key.lower() == 'q':
                    break
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    clearScreen()

def simplePlayback(board, steps, startStep=0):
    for i in range(startStep, len(steps)):
        clearScreen()
        stepNum, dir, pos = steps[i]
        if stepNum == 0:
            print("="*45)
            print("Initial State")
            print("="*45)
        else:
            print("="*45)
            print(f"Step {stepNum}: {dir}")
            print("="*45)
        displayBoard(board, pos)
        print(f"\nStep {i}/{len(steps)-1}")
        print("Press ENTER to continue...")
        input()

def saveSolution(board, res, steps, filepath):
    with open(filepath, 'w') as f:
        f.write("="*45 + "\n")
        f.write("Ice Sliding Puzzle Solution\n")
        f.write("="*45 + "\n\n")
        f.write(f"Solution Path: {res['solution']}\n")
        f.write(f"Total Cost: {res['cost']}\n")
        f.write(f"Iterations: {res['iterations']}\n\n")
        f.write("="*45 + "\n")
        f.write("Step-by-step Solution\n")
        f.write("="*45 + "\n\n")
        for stepNum, dir, pos in steps:
            if stepNum == 0:
                f.write(f"Initial State:\n")
            else:
                f.write(f"Step {stepNum}: {dir}\n")
            #write state boardnya
            for i in range(board.rows):
                rowStr = ""
                for j in range(board.cols):
                    if (i, j) == pos:
                        rowStr += "Z"
                    else:
                        rowStr += board.grid[i][j]
                f.write(rowStr + "\n")
            f.write("\n")
        f.write("="*45 + "\n")
        f.write("End of Solution\n")
        f.write("="*45 + "\n")

def main():
    #minta input file
    print(">> Masukan file input :")
    file_path = input().strip()
    try:
        board = parse_file(file_path)
        print(f"Board loaded: {board.rows}x{board.cols}")
    except Exception as e:
        print(f"Error loading file: {e}")
        return
    #pilih algoritma
    print("\n>> Algoritma apa yang anda pilih? (UCS/GBFS/A*)")
    algo = input().strip().upper()
    if algo not in ['UCS', 'GBFS', 'A*']:
        print("Invalid choice")
        return
    #pilih heuristic jika GBFS atau A*
    heuristic = None
    heuChoice = None
    if algo in ['GBFS', 'A*']:
        print("\n>> Heuristic apa yang anda pilih? (H1/H2/H3)")
        heuChoice = input().strip().upper()
        heuristic = getHeuristic(heuChoice)
        if heuristic is None:
            print("Invalid choice")
            return
    #jalankan algoritma
    print("\n>> Mencari solusi...")
    startTime = time.time()
    if algo == 'UCS':
        result = ucs(board)
    elif algo == 'GBFS':
        result = gbfs(board, heuristic)
    elif algo == 'A*':
        print("Belum diimplement!")
        return
    endTime = time.time()
    execTime = (endTime - startTime) * 1000  #convert ke ms
    #display hasil
    if not result['found']:
        print("\n" + "="*45)
        print("Tidak ada solusi yang ditemukan")
        print(f"Waktu eksekusi: {execTime:.2f} ms")
        print(f"Node yang dieksplorasi: {result['iterations']}")
        print("="*45)
        return
    #generate step-by-step solution
    steps = getSolutionSteps(board, result['solution'])
    #tampilkan hasil
    print("\n" + "="*45)
    print(f"Solusi Yang Ditemukan : {result['solution']}")
    print(f"Cost dari Solusi : {result['cost']}")
    print("="*45)
    #display semua steps
    for stepNum, dir, pos in steps:
        if stepNum == 0:
            print("\nInitial")
        else:
            print(f"\nStep {stepNum} : {dir}")
        
        displayBoard(board, pos)
    print("="*45)
    print(f">> Waktu eksekusi: {execTime:.2f} ms")
    print(f">> Banyak iterasi yang dilakukan: {result['iterations']} iterasi")
    print("="*45)
    #opsi playback
    print("\n>> Apakah Anda ingin melakukan playback? (Ya/Tidak) :")
    playbackChoice = input().strip().lower()
    if playbackChoice in ['ya', 'y', 'yes']:
        print("\n>> Pada step berapa anda ingin melakukan playback :")
        try:
            startStep = int(input().strip())
            if 0 <= startStep < len(steps):
                #coba masukin ke mode playback interaktif
                try:
                    playback(board, steps)
                except:
                    # Fallback to simple playback
                    print("\nInteractive mode not supported, using simple playback...")
                    time.sleep(1)
                    simplePlayback(board, steps, startStep)
            else:
                print(f"Step harus berada di antara 0 dan {len(steps)-1}")
        except ValueError:
            print("Invalid input, skipping playback")
    #opsi save solusi
    print("\n>> Apakah Anda ingin menyimpan solusi? (Ya/Tidak) :")
    saveChoice = input().strip().lower()
    if saveChoice in ['ya', 'y', 'yes']:
        #bikin output directory kalau ga exist
        output_dir = "output"
        os.makedirs(output_dir, exist_ok=True)
        #generate filename
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        outputfilename = f"{output_dir}/solution_{algo}_{timestamp}.txt"
        if heuChoice:
            outputfilename = f"{output_dir}/solution_{algo}_{heuChoice}_{timestamp}.txt"
        saveSolution(board, result, steps, outputfilename)
        #ambil path absolut
        absPath = os.path.abspath(outputfilename)
        print(f"\n>> Solusi disimpan pada {absPath}")
    print("\nProgram selesai")

if __name__ == "__main__":
    main()