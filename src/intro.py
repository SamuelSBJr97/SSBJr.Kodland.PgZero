import pgzrun
import math
import random
from pgzero.actor import Actor
from pgzero.keyboard import keyboard

class BattleBugs:
    
    def __init__(self):
        self.reset()

    def reset(self):
        self.board = []
        self.boardsSelecteds = []
        self.bugs = []
        self.bullets = []
        self.objects = []
        self.player: Actor

    def start(self):
        self.board = []
        # algoritmo para gerar chão que o player e bugs podem andar
        for x in range(16):
            for y in range(10):
                if random.random() < 0.8:
                    floor = Actor('floor')
                    floor.images = ['floor']
                    floor.x = x * 50 + 25
                    floor.y = y * 50 + 25 + 50
                    self.board.append(floor)

        self.boardsSelecteds = []

        self.bugs = []
        for _ in range(5):
            bug = Actor('bug-1', anchor=('center', 'center'))
            bug.images = ['bug-1', 'bug-2', 'bug-3', 'bug-4']
            bug.angle = 0

            _board = random.choice(list(filter(lambda b: b not in self.boardsSelecteds, self.board)))

            self.boardsSelecteds.append(_board)
            bug.x = _board.x
            bug.y = _board.y
            self.bugs.append(bug)

        self.player = Actor("player-1", anchor=('center', 'center'))
        self.player.images = ['player-1', 'player-2', 'player-3', 'player-4']
        self.player.angle = 0

        # garante que o player não comece em cima de um bug
        _board = random.choice(list(filter(lambda b: b not in self.boardsSelecteds, self.board)))

        self.player.x = _board.x
        self.player.y = _board.y

        # passa referencia dos objetos para facilitar o draw/update
        self.objects = [*self.board, *self.bugs, self.player]

    def next_board(self, actor, forward=True, bullet=False):
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
            for _board in self.board:
                if x == _board.x and y == _board.y:
                    actor.x = _board.x
                    actor.y = _board.y
                    hasBoard = True
                    break
        elif not bullet:
            for _board in self.boardsSelecteds:
                if actor.x == _board.x and actor.y == _board.y:
                    boardSelected = self.boardsSelecteds.index(_board)

            for _board in self.board:
                if x == _board.x and y == _board.y and _board not in self.boardsSelecteds:
                    actor.x = _board.x
                    actor.y = _board.y
                    self.boardsSelecteds.append(_board)
                    hasBoard = True
                    break

            if hasBoard and boardSelected is not None:
                del self.boardsSelecteds[boardSelected]

        return hasBoard

    def actor_anime(self, actor: Actor):
        angle = actor.angle
        actor.image = actor.images[random.randint(0, len(actor.images) - 1)]
        actor.angle = angle

# Inicializa o jogo
battleBugs = BattleBugs()

def on_key_down(key):
    if keyboard.Escape:
        battleBugs.reset()
        return

    if keyboard.left or keyboard.right or keyboard.up or keyboard.down:
        angle = battleBugs.player.angle

        # right or left fica girando
        if keyboard.right or keyboard.left:
            if keyboard.right:
                angle -= 90
            elif keyboard.left:
                angle += 90
            
            angle = angle % 360

            battleBugs.player.angle = angle

        elif keyboard.up or keyboard.down:
            battleBugs.next_board(battleBugs.player, keyboard.up == True)

    elif keyboard.space:
        bullet = Actor('bullet-1', anchor=('center', 'center'))
        bullet.images = ['bullet-1', 'bullet-2', 'bullet-3']
        bullet.angle = battleBugs.player.angle
        bullet.x = battleBugs.player.x
        bullet.y = battleBugs.player.y
        battleBugs.objects.append(bullet)
        battleBugs.bullets.append(bullet)

    if len(battleBugs.bugs) > 0 and (keyboard.left or keyboard.right or keyboard.up or keyboard.down or keyboard.space):
        bug = random.choice(battleBugs.bugs)

        # Calcula a diferença de posição entre o bug e o player
        dx = abs(battleBugs.player.x - bug.x)
        dy = abs(battleBugs.player.y - bug.y)

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
        battleBugs.next_board(bug, dx < dy)

def update(dt):
    for bullet in battleBugs.bullets:
        hasHit = False
        for bug in battleBugs.bugs:
            if bug.x == bullet.x and bug.y == bullet.y:
                hasHit = True
                battleBugs.objects.remove(bug)
                battleBugs.bugs.remove(bug)

                for _board in battleBugs.boardsSelecteds:
                    if bug.x == _board.x and bug.y == _board.y:
                        battleBugs.boardsSelecteds.remove(_board)
                        break
                break

        if hasHit or not battleBugs.next_board(bullet, True, True):
            battleBugs.objects.remove(bullet)
            battleBugs.bullets.remove(bullet)

def draw():
    screen.clear()

    for obj in battleBugs.objects:
        battleBugs.actor_anime(obj)
        obj.draw()

    screen.draw.text(f'Bugs restantes: {len(battleBugs.bugs)}', (10, 10), color='white')

pgzrun.go()