import pygame
import random
import time


def printInstructions():
    file = open("Instrukcja_Sterowania.txt")
    print(file.read())
    file.close()


def initGlobal():
    print("Inicjalizacja symulatora...")
    time.sleep(1)
    initGlobalValues()
    initColours()


def initGlobalValues():
    global WINDOW_SIZE, OPTION, WIDTH, HEIGHT, MARGIN, DONE, SPEED, STOP, BOARD, NUMBER_OF_BOARDS, minX, maxX
    global cacheMinX, cacheMaxX
    WINDOW_SIZE = [755, 755]
    OPTION = 0
    WIDTH = 20
    HEIGHT = 20
    MARGIN = 5
    DONE = False
    SPEED = 10
    STOP = False
    BOARD = 0
    NUMBER_OF_BOARDS = 5
    minX = 0
    maxX = 29
    cacheMinX = 0
    cacheMaxX = 29


def initColours():
    global BLOCKED, BLACK, WHITE, YELLOW
    BLOCKED = (128, 128, 128)
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    YELLOW = (194, 178, 128)


def initWindow():
    global screen, clock
    print("Przygotowanie okna symulatora...")
    time.sleep(1)
    pygame.init()
    screen = pygame.display.set_mode(WINDOW_SIZE)
    screen.fill(BLACK)
    pygame.display.set_caption("Sand fall simulator")
    clock = pygame.time.Clock()


def readBlockFieldsFromFile(filename):
    global minX, maxX, cacheMinX, cacheMaxX
    blockFields = []
    file = open(filename)
    fileLines = file.read().split("\n")
    file.close()
    for i in range(len(fileLines) - 1):
        row, column = fileLines[i].split(" ")
        blockFields.append((int(row), int(column)))

    limits = fileLines[len(fileLines) - 1].split(" ")

    minX = int(limits[0])
    maxX = int(limits[1])
    cacheMinX = minX
    cacheMaxX = maxX

    return blockFields


def createBlockFields(blockFields):
    global grid, screen, BLOCKED, MARGIN, WIDTH, HEIGHT
    for blockField in blockFields:
        grid[blockField[0]][blockField[1]] = -1
        pygame.draw.rect(screen, BLOCKED, [(MARGIN + WIDTH) * blockField[1] + MARGIN,
                        (MARGIN + HEIGHT) * blockField[0] + MARGIN, WIDTH, HEIGHT])


def prepareGrid():
    global OPTION
    if OPTION == 0:
        return prepareMargolusGrids()
    else:
        return prepareShiftedMargolusGrids()


def prepareMargolusGrids():
    global OPTION
    print("Generowanie siatki Margolusa...")
    margolusGrids = []
    for row in range(OPTION, 30, 2):
        counter = 0
        while counter < 30:
            table = []
            table.append((row, counter))
            table.append((row, (counter + 1) % 30))
            table.append(((row + 1) % 30, counter))
            table.append(((row + 1) % 30, (counter + 1) % 30))
            if len(table) != 0:
                margolusGrids.append(table)
            counter += 2

    if OPTION:
        OPTION = 0
    else:
        OPTION = 1
    return margolusGrids


def prepareShiftedMargolusGrids():
    global OPTION
    print("Generowanie przesuniętej siatki Margolusa...")
    margolusGrids = []
    margolusGrids.append([(0,0)])
    for i in range(1, 29, 2):
        margolusGrids.append([(0, i), (0, i + 1)])
    margolusGrids.append([(0, 29)])
    for row in range(1, 29, 2):
        counter = 1
        margolusGrids.append([(row, 0), (row + 1, 0)])
        while counter < 30:
            table = []
            table.append((row, counter))
            if counter != 29:
                table.append((row, counter + 1))
            if row != 29:
                table.append((row + 1, counter))
            if row != 29 and counter != 29:
                table.append(((row + 1) % 30, (counter + 1) % 30))
            if len(table) != 0:
                margolusGrids.append(table)
            counter += 2
        margolusGrids.append(table)

        margolusGrids.append([(row, 29), (row + 1, 29)])

    if OPTION:
        OPTION = 0
    else:
        OPTION = 1
    return margolusGrids


def sandFall():
    margolusGrids = prepareGrid()
    for row in margolusGrids:
        if len(row) == 1:
            #VI
            continue
        if len(row) == 2:
            if row[0][0] != row[1][0] and grid[row[0][0]][row[0][1]] == 1 and grid[row[1][0]][row[1][1]] == 0:
                grid[row[0][0]][row[0][1]] = 0
                grid[row[1][0]][row[1][1]] = 1
                print(f"Piasek spada z pola ({row[0][0]}, {row[0][1]}) na pole ({row[1][0]}, {row[1][1]})")
            continue
        if grid[row[0][0]][row[0][1]] == 1 and grid[row[2][0]][row[2][1]] == 0:
            #I
            grid[row[0][0]][row[0][1]] = 0
            grid[row[2][0]][row[2][1]] = 1
            print(f"Piasek spada z pola ({row[0][0]}, {row[0][1]}) na pole ({row[2][0]}, {row[2][1]})")
        if grid[row[1][0]][row[1][1]] == 1 and grid[row[3][0]][row[3][1]] == 0:
            #II
            grid[row[1][0]][row[1][1]] = 0
            grid[row[3][0]][row[3][1]] = 1
            print(f"Piasek spada z pola ({row[1][0]}, {row[1][1]}) na pole ({row[3][0]}, {row[3][1]})")
        if grid[row[0][0]][row[0][1]] == 1 and grid[row[2][0]][row[2][1]] == 1 and grid[row[3][0]][row[3][1]] == 0:
            #III
            grid[row[0][0]][row[0][1]] = 0
            grid[row[3][0]][row[3][1]] = 1
            print(f"Piasek spada z pola ({row[0][0]}, {row[0][1]}) na pole ({row[3][0]}, {row[3][1]})")
        if grid[row[1][0]][row[1][1]] == 1 and grid[row[3][0]][row[3][1]] == 1 and grid[row[2][0]][row[2][1]] == 0:
            #IV
            grid[row[1][0]][row[1][1]] = 0
            grid[row[2][0]][row[2][1]] = 1
            print(f"Piasek spada z pola ({row[1][0]}, {row[1][1]}) na pole ({row[2][0]}, {row[2][1]})")
        if grid[row[0][0]][row[0][1]] == 1 and grid[row[1][0]][row[1][1]] == 1 and grid[row[2][0]][row[2][1]] == 0 and grid[row[3][0]][row[3][1]] == 0:
            #V
            grid[row[0][0]][row[0][1]] = 0
            grid[row[1][0]][row[1][1]] = 0
            grid[row[2][0]][row[2][1]] = 1
            grid[row[3][0]][row[3][1]] = 1
            print(f"Piasek spada z pola ({row[0][0]}, {row[0][1]}) na pole ({row[1][0]}, {row[1][1]})")
            print(f"Piasek spada z pola ({row[2][0]}, {row[2][1]}) na pole ({row[3][0]}, {row[3][1]})")


def runSimulator():
    print("Uruchamianie symulatora...")
    time.sleep(1)
    counter = 0
    while not DONE:
        eventsHandler()
        if STOP:
            continue
        sandFall()
        updateFields()
        sandGenerator(counter)
        updateScreen()
        counter += 1


def eventsHandler():
    global DONE, STOP, SPEED, BOARD, NUMBER_OF_BOARDS, minX, maxX, cacheMinX, cacheMaxX
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print("Zamykanie symulatora...")
            time.sleep(1)
            DONE = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if STOP:
                    print("Symulator wznawia pracę")
                    STOP = False
                else:
                    print("Symulator został zatrzymany")
                    STOP = True
            elif event.key == pygame.K_UP:
                SPEED += 5
                print(f"Prędkość symulacji został zwiększona. Obecna prędkość: {SPEED}")
            elif event.key == pygame.K_DOWN:
                if SPEED != 5:
                    print(f"Prędkość symulacji została zmniejszona. Obecna prędkość: {SPEED}")
                    SPEED -= 5
            elif event.key == pygame.K_r:
                print("Plansza została zresetowana")
                resetBoard()
            elif event.key == pygame.K_q:
                print("Zamykanie symulatora...")
                time.sleep(1)
                DONE = True
            elif event.key == pygame.K_RIGHT:
                BOARD = (BOARD + 1) % NUMBER_OF_BOARDS
                print(f"Plansza została zmieniona. ID obecnej planszy: {BOARD}")
                resetBoard()
            elif event.key == pygame.K_LEFT:
                if BOARD == 0:
                    BOARD = NUMBER_OF_BOARDS - 1
                else:
                    BOARD -= 1
                print(f"Plansza została zmieniona. ID obecnej planszy: {BOARD}")
                resetBoard()
            elif event.key == pygame.K_1:
                print("Zmiana sposobu generowania piasku. Piasek generowany nad naczyniem.")
                maxX = cacheMaxX
                minX = cacheMinX
            elif event.key == pygame.K_2:
                print("Zmiana sposobu generowania piasku. Piasek generowany na całej krawędzi.")
                minX = 0
                maxX = 29


def resetBoard():
    createFields()


def updateFields():
    global grid
    for row in range(30):
        for column in range(30):
            if grid[row][column] == -1:
                color = BLOCKED
            elif grid[row][column] == 1:
                color = YELLOW
            else:
                color = WHITE
            pygame.draw.rect(screen, color, [(MARGIN + WIDTH) * column + MARGIN, (MARGIN + HEIGHT) * row + MARGIN,
                            WIDTH, HEIGHT])


def sandGenerator(counter):
    global grid, minX, maxX
    if counter % 3 == 0:
        number = random.randint(0, maxX)
        for i in range(number):
            col = random.randint(minX, maxX)
            grid[0][col] = 1
            color = YELLOW
            pygame.draw.rect(screen, color, [(MARGIN + WIDTH) * col + MARGIN, (MARGIN + HEIGHT) * 0 + MARGIN,
                            WIDTH, HEIGHT])
            print(f"Piasek został wygenerowany na polu ({0}, {col})")


def updateScreen():
    global clock, SPEED
    clock.tick(SPEED)
    pygame.display.flip()


def createFields():
    global grid
    print("Przygotowanie pól planszy...")
    grid = []
    for row in range(30):
        grid.append([])
        for column in range(30):
            grid[row].append(0)
    updateBlockFields()


def updateBlockFields():
    global BOARD
    blockFields = readBlockFieldsFromFile("Boards/Board_" + str(BOARD) + ".txt")
    createBlockFields(blockFields)


if __name__ == "__main__":
    printInstructions()
    initGlobal()
    initWindow()
    createFields()
    runSimulator()
    pygame.quit()
