import math
import random

def reset():
    global objects
    global player
    global board
    global bugs

    board = []
    # algoritmo para gerar chão que o player e bugs podem andar
    for x in range(16):
        for y in range(10):
            if random.random() < 0.8:
                floor = Actor('floor')
                floor.x = x * 50 + 25
                floor.y = y * 50 + 25 + 50
                board.append(floor)

    _boardsSelecteds = []

    bugs = []
    for _ in range(5):
        bug = Actor('bug-1', anchor=('center', 'center'))
        bug.images = ['bug-1', 'bug-2', 'bug-3', 'bug-4']
        bug.angle = 0

        while True:
            _board = random.choice(board)
            if _board in _boardsSelecteds:
                continue

            _boardsSelecteds.append(_board)
            bug.x = _board.x
            bug.y = _board.y
            bugs.append(bug)

            break

    player = Actor("player-1", anchor=('center', 'center'))
    player.images = ['player-1', 'player-2', 'player-3', 'player-4']
    player.angle = 0

    # garante que o player não comece em cima de um bug
    while True:
        _board = random.choice(board)
    
        if _board in _boardsSelecteds:
            continue

        player.x = _board.x
        player.y = _board.y

        break

    objects = [*board, *bugs, player]

reset()

def update(dt):
    angle = player.angle

    if keyboard.right:
        angle = 270

    if keyboard.left:
        angle = 90

    if keyboard.up:
        angle = 0

    if keyboard.down:
        angle = 180

    player.image = player.images[random.randint(0, len(player.images) - 1)]
    player.angle = angle

    for bug in bugs:
        bug.image = bug.images[random.randint(0, len(bug.images) - 1)]

    if keyboard.space:
        pass

    if keyboard.ESCAPE:
        reset()

def draw():
    screen.clear()

    for obj in objects:
        obj.draw()