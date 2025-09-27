import sys
import pgzrun
import math
import random
from pgzero.actor import Actor
from pgzero.keyboard import keyboard
from pgzero import tone
from pgzero.clock import clock

class BattleBugs:
    
    def __init__(self):
        self.reset()
        self.start()

    def reset(self):
        self.board = []
        self.boardsSelecteds = []
        self.bugs = []
        self.bullets = []
        self.objects = []
        self.player: Actor
        self.som = True
        self.state = 'intro'  # intro, start, gameover
        self.bug_image: Actor
        self.player_image: Actor
        # (tema removido) não mais inicializa música de fundo aqui

    def start(self):
        self.bug_image = Actor('bug-1', anchor=('center', 'center'))
        self.bug_image.x = 400
        self.bug_image.y = 250

        self.player_image = Actor('player-1', anchor=('center', 'center'))
        self.player_image.x = 400
        self.player_image.y = 150

        self.board = []
        for x in range(16):
            for y in range(10):
                floor = Actor('floor')
                floor.images = ['floor']
                floor.x = x * 50 + 25
                floor.y = y * 50 + 25 + 50
                self.board.append(floor)

        self.objects = [*self.board]

    def players(self):
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

            # Som de movimento (nota curta) — respeita self.som quando actor for player ou bug
            try:
                if hasBoard and self.som:
                    # som de movimento mais grave
                    tone.play('G3', 0.06)
            except Exception:
                pass

        return hasBoard

    def actor_anime(self, actor: Actor):
        angle = actor.angle
        actor.image = actor.images[(actor.images.index(actor.image) + 1) % len(actor.images)] # algoritmo que verifica a imagem atual e determina a proxima com base na lista de imagems
        actor.angle = angle
    

    def key_down(self, keyboard):
        if self.state == 'intro':
            if keyboard.RETURN:
                # inicia o jogo
                self.state = 'game'
                self.players()
            if keyboard.m:
                # ativa/desativa o som
                self.som = not self.som
            if keyboard.Escape:
                # encerra o jogo
                sys.exit()

        elif self.state == 'game':
            if keyboard.Escape:
                self.state = 'intro'
                self.reset()
                self.start()
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

                # Som de disparo — respeita self.som
                try:
                    if self.som:
                        # som de disparo mais grave
                        tone.play('F#4', 0.08)
                except Exception:
                    pass

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
                # Som de explosão quando um bug é acertado
                try:
                    if hasHit and self.som:
                        # explosão mais grave e longa
                        tone.play('C2', 0.20)
                        # nota de ressonância após 0.12s (grave)
                        clock.schedule_unique(lambda: tone.play('G2', 0.14), 0.12)
                except Exception:
                    pass

    def draw(self, screen, keyboard):
        screen.clear()

        for obj in self.objects:
            self.actor_anime(obj)
            obj.draw()

        if self.state == 'intro':
            screen.draw.text('Bem-vindo ao Battle Bugs!', center=(400, 50), color='white', fontsize=40)
            # adicione os controles e objetivos do jogo aqui
            screen.draw.text('Use as setas para mover e a barra de espaço para atirar', center=(400, 100), color='white', fontsize=40)
            self.player_image.draw()
            
            screen.draw.text('Dispare nos bugs!', center=(400, 200), color='white', fontsize=40)
            self.bug_image.draw()

            screen.draw.text('Tecle Enter para iniciar', center=(400, 350), color='white', fontsize=40)
            screen.draw.text(f'Som {"ativado" if self.som else "desativado"}. Tecle M para {"desativar" if self.som else "ativar"}', center=(400, 400), color='white', fontsize=40) # texto formatado de acordo com o estado do som
            screen.draw.text('Tecle Esc para encerrar', center=(400, 450), color='white', fontsize=40)
        if self.state == 'game' and len(self.bugs) == 0:
            screen.draw.text('Parabéns! Você venceu!', center=(400, 250), color='white', fontsize=40)
            screen.draw.text('Tecle Esc para reiniciar', center=(400, 300), color='white', fontsize=40)
        if self.state == 'game' and len(self.bugs) > 0:
            screen.draw.text(f'Bugs restantes: {len(self.bugs)}', topright=(790, 10), color='white', fontsize=30)

# Inicializa o jogo
battleBugs = BattleBugs()

def on_key_down(key):
    battleBugs.key_down(keyboard)

def update(dt):
    battleBugs.update(dt, keyboard)

def draw():
    battleBugs.draw(screen, keyboard)

pgzrun.go()