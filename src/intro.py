import sys
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
        self.som = True
        self.state = 'intro'  # intro, start, gameover

    def intro(self, screen):
        if len(self.board) > 0:
            return
        
        # algoritmo para gerar chão que o player e bugs podem andar
        for x in range(16):
            for y in range(10):
                if random.random() < 0.8:
                    floor = Actor('floor')
                    floor.images = ['floor']
                    floor.x = x * 50 + 25
                    floor.y = y * 50 + 25 + 50
                    self.board.append(floor)

        self.objects = [*self.board]

        screen.draw.text(f'Bugs restantes: {len(self.bugs)}', (10, 10), color='white')

    def start(self):
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

        self.objects = []
        # passa referencia dos objetos para facilitar o draw/update
        self.objects = [*self.board, *self.bugs, self.player]

        self.state = 'game'

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

    def key_down(self, keyboard):
        if self.state != 'game':
            return

        if keyboard.Escape:
            self.reset()
            return

        if keyboard.left or keyboard.right or keyboard.up or keyboard.down:
            angle = self.player.angle

            # right or left fica girando
            if keyboard.right or keyboard.left:
                if keyboard.right:
                    angle -= 90
                elif keyboard.left:
                    angle += 90
                
                angle = angle % 360

                self.player.angle = angle

            elif keyboard.up or keyboard.down:
                self.next_board(self.player, keyboard.up == True)

        elif keyboard.space:
            bullet = Actor('bullet-1', anchor=('center', 'center'))
            bullet.images = ['bullet-1', 'bullet-2', 'bullet-3']
            bullet.angle = self.player.angle
            bullet.x = self.player.x
            bullet.y = self.player.y
            self.objects.append(bullet)
            self.bullets.append(bullet)

        if len(self.bugs) > 0 and (keyboard.left or keyboard.right or keyboard.up or keyboard.down or keyboard.space):
            bug = random.choice(self.bugs)

            # Calcula a diferença de posição entre o bug e o player
            dx = abs(self.player.x - bug.x)
            dy = abs(self.player.y - bug.y)

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
            self.next_board(bug, dx < dy)

    def update(self, dt, keyboard):
        if self.state != 'game':
            return

        for bullet in self.bullets:
            hasHit = False
            for bug in self.bugs:
                if bug.x == bullet.x and bug.y == bullet.y:
                    hasHit = True
                    self.objects.remove(bug)
                    self.bugs.remove(bug)

                    for _board in self.boardsSelecteds:
                        if bug.x == _board.x and bug.y == _board.y:
                            self.boardsSelecteds.remove(_board)
                            break
                    break

            if hasHit or not self.next_board(bullet, True, True):
                self.objects.remove(bullet)
                self.bullets.remove(bullet)

    def draw(self, screen, keyboard):
        screen.clear()

        for obj in self.objects:
            self.actor_anime(obj)
            obj.draw()

        if self.state == 'intro':
            self.intro(screen)
            screen.draw.text('Tecle Enter para iniciar', center=(400, 250), color='white', fontsize=40)
            screen.draw.text('Som ativado. Tecle M para desativar', center=(400, 300), color='white', fontsize=40)
            screen.draw.text('Tecle Esc para encerrar', center=(400, 350), color='white', fontsize=40)
            if keyboard.RETURN:
                self.state = 'start'
            if keyboard.m:
                # ativa/desativa o som
                self.som = not self.som
            if keyboard.Escape:
                # encerra o jogo
                sys.exit()
        elif self.state == 'start':
            self.start()

# Inicializa o jogo
battleBugs = BattleBugs()

def on_key_down(key):
    battleBugs.key_down(keyboard)

def update(dt):
    battleBugs.update(dt, keyboard)

def draw():
    battleBugs.draw(screen, keyboard)

pgzrun.go()