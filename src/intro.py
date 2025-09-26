import math
import random

def reset():
    global objects
    global player
    global board
    global path
    global bugs

    player = Actor("player", anchor=('center', 'center'), pos=(400, 300))
    img_player = 'player'

    board = []
    path = []
    bugs = []
    #for _ in range(5):
    #    bug = Actor("bug", (random.randint(0, 800), random.randint(0, 600)))
    #    bugs.append(bug)

    objects = [*bugs, *board, *path, player]

reset()

def update(dt):
    original_x = player.x
    original_y = player.y

    img_player = player.image
    angle = player.angle

    if keyboard.right:
        player.x += 1
        img_player = 'player'
        angle = 0

    if keyboard.left:
        player.x -= 1
        img_player = 'player-left'
        angle = 180

    if keyboard.up:
        player.y -= 1
        angle = 90

    if keyboard.down:
        player.y += 1
        angle = 270

    player.image = img_player
    player.angle = angle

    if keyboard.space:
        pass

    if keyboard.ESCAPE:
        reset()

    if player.x < 0 or player.x > 800 or player.y < 0 or player.y > 600:
        player.x = original_x
        player.y = original_y

def draw():
    screen.clear()

    for obj in objects:
        obj.draw()