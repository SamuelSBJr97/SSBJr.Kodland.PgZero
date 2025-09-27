import pgzrun
import math
import random
from pgzero.actor import Actor
from pgzero.keyboard import keyboard

def reset():
    global objects
    global player
    global board
    global boardsSelecteds
    global bugs
    global bullets

    board = []
    # algoritmo para gerar chão que o player e bugs podem andar
    for x in range(16):
        for y in range(10):
            if random.random() < 0.8:
                floor = Actor('floor')
                floor.images = ['floor']
                floor.x = x * 50 + 25
                floor.y = y * 50 + 25 + 50
                board.append(floor)

    boardsSelecteds = []

    bugs = []
    for _ in range(5):
        bug = Actor('bug-1', anchor=('center', 'center'))
        bug.images = ['bug-1', 'bug-2', 'bug-3', 'bug-4']
        bug.angle = 0

        while True:
            _board = random.choice(board)
            if _board in boardsSelecteds:
                continue

            boardsSelecteds.append(_board)
            bug.x = _board.x
            bug.y = _board.y
            bugs.append(bug)

            break

    bullets = []

    player = Actor("player-1", anchor=('center', 'center'))
    player.images = ['player-1', 'player-2', 'player-3', 'player-4']
    player.angle = 0

    # garante que o player não comece em cima de um bug
    while True:
        _board = random.choice(board)
    
        if _board in boardsSelecteds:
            continue

        player.x = _board.x
        player.y = _board.y

        break

    # passa referencia dos objetos para facilitar o draw/update
    objects = [*board, *bugs, player]

reset()

def next_board(actor, forward=True, bullet=False):
    x = actor.x
    y = actor.y

    if forward:
        if actor.angle == 0:   # cima
            y -= 50
        elif actor.angle == 90:  # esquerda
            x -= 50
        elif actor.angle == 180: # baixo
            y += 50
        elif actor.angle == 270: # direita
            x += 50
    else:
        if actor.angle == 0:   # cima
            y += 50
        elif actor.angle == 90:  # esquerda
            x += 50
        elif actor.angle == 180: # baixo
            y -= 50
        elif actor.angle == 270: # direita
            x -= 50

    hasBoard = False
    boardSelected = None

    if bullet:
        for _board in board:
            if x == _board.x and y == _board.y:
                actor.x = _board.x
                actor.y = _board.y
                hasBoard = True
                break
    elif not bullet:
        for _board in boardsSelecteds:
            if actor.x == _board.x and actor.y == _board.y:
                boardSelected = boardsSelecteds.index(_board)

        for _board in board:
            if x == _board.x and y == _board.y and _board not in boardsSelecteds:
                actor.x = _board.x
                actor.y = _board.y
                boardsSelecteds.append(_board)
                hasBoard = True
                break

        if hasBoard and boardSelected is not None:
            del boardsSelecteds[boardSelected]

    return hasBoard

def actor_anime(actor):
    angle = actor.angle
    actor.image = actor.images[random.randint(0, len(actor.images) - 1)]
    actor.angle = angle

def on_key_down(key):
    if keyboard.Escape:
        reset()
        return

    if keyboard.left or keyboard.right or keyboard.up or keyboard.down:
        angle = player.angle

        # right or left fica girando
        if keyboard.right or keyboard.left:
            if keyboard.right:
                angle -= 90
            elif keyboard.left:
                angle += 90
            
            angle = angle % 360

            player.angle = angle

        elif keyboard.up or keyboard.down:
            next_board(player, keyboard.up == True)

    elif keyboard.space:
        bullet = Actor('bullet-1', anchor=('center', 'center'))
        bullet.images = ['bullet-1', 'bullet-2', 'bullet-3']
        bullet.angle = player.angle
        bullet.x = player.x
        bullet.y = player.y
        objects.append(bullet)
        bullets.append(bullet)

    if len(bugs) > 0 and (keyboard.left or keyboard.right or keyboard.up or keyboard.down or keyboard.space):
        bug = random.choice(bugs)

        # Calcula a diferença de posição entre o bug e o player
        dx = abs(player.x - bug.x)
        dy = abs(player.y - bug.y)

        # Decide a direção prioritária para o bug se mover em direção ao player
        if dx > dy:
            # Move horizontalmente
            if dx > 0:
                angle = 270  # direita
            else:
                angle = 90   # esquerda
        else:
            # Move verticalmente
            if dy > 0:
                angle = 180  # baixo
            else:
                angle = 0    # cima

        bug.angle = angle
        next_board(bug, dx < dy)

def update(dt):
    for bullet in bullets:
        hasHit = False
        for bug in bugs:
            if bug.x == bullet.x and bug.y == bullet.y:
                hasHit = True
                objects.remove(bug)
                bugs.remove(bug)

                for _board in boardsSelecteds:
                    if bug.x == _board.x and bug.y == _board.y:
                        boardsSelecteds.remove(_board)
                        break
                break

        if hasHit or not next_board(bullet, True, True):
            objects.remove(bullet)
            bullets.remove(bullet)

def draw():
    screen.clear()

    for obj in objects:
        actor_anime(obj)
        obj.draw()

    screen.draw.text(f'Bugs restantes: {len(bugs)}', (10, 10), color='white')

pgzrun.go()