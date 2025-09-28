import sys
import pgzrun
import math
import random
from pgzero.actor import Actor
from pgzero.keyboard import keyboard
from pgzero import tone
from pgzero import music as pgz_music
from pgzero.animation import animate
from pgzero.clock import clock

class BattleBugs:
    
    def __init__(self):
        self.som = True
        self.som_playing = False

        self.reset()
        self.start()

    def reset(self):
        self.board: Actor
        self.boardsSelecteds = []
        self.bugs = []
        self.bullets = []
        self.objects = []
        self.player: Actor
        self.state = 'intro'  # intro, start, gameover
        self.bug_image: Actor
        self.player_image: Actor

    def start(self):
        self.bug_image = Actor('bug-1', anchor=('center', 'center'))
        self.bug_image.images = ['bug-1', 'bug-2', 'bug-3', 'bug-4']
        self.bug_image.x = 400
        self.bug_image.y = 250

        self.player_image = Actor('player-1', anchor=('center', 'center'))
        self.player_image.images = ['player-1', 'player-2', 'player-3', 'player-4']
        self.player_image.x = 400
        self.player_image.y = 150

        self.board = Actor('floor-550x800', anchor=('center', 'center'))
        self.board.x = 400
        self.board.y = 325

        self.objects = [self.board]

        self.play_theme()

    def play_theme(self):
        """Tenta iniciar a reprodução do tema em loop, respeitando self.som."""
        # usa somente a API do pgzero - requer que exista music/tema.mp3
        try:
            if not self.som or self.som_playing:
                return
            pgz_music.play('tema')
            pgz_music.set_volume(0.1)  # volume mais baixo para não incomodar
            self.som_playing = True
        except Exception:
            # não crashar se algo falhar; talvez o arquivo não exista
            pass

    def stop_theme(self):
        """Para a reprodução do tema (fade out não usado para simplicidade)."""
        try:
            pgz_music.stop()
            self.som_playing = False
        except Exception:
            pass

    def players(self):
        self.bugs = []
        for _ in range(5):
            bug = Actor('bug-1', anchor=('center', 'center'))
            bug.images = ['bug-1', 'bug-2', 'bug-3', 'bug-4']
            bug.angle = 0

            bug.x = random.randint(1, 7) * 50
            bug.y = random.randint(1, 9) * 50 + 50
            self.bugs.append(bug)

        self.player = Actor("player-1", anchor=('center', 'center'))
        self.player.images = ['player-1', 'player-2', 'player-3', 'player-4']
        self.player.angle = 0

        self.player.x = random.randint(1, 7) * 50
        self.player.y = random.randint(1, 9) * 50 + 50

        # passa referencia dos objetos para facilitar o draw/update
        self.objects = [self.board, *self.bugs, self.player]

    def next_board(self, actor, animate, forward=True, bullet=False):
        x = actor.x
        y = actor.y
        step = 50

        # Calcula deslocamento baseado no ângulo do ator.
        # Convenção: angle=0 => cima; angle aumenta no sentido anti-horário.
        # Fórmulas escolhidas para manter compatibilidade com o mapeamento anterior:
        # dx = -sin(rad) * step, dy = -cos(rad) * step
        try:
            rad = math.radians(actor.angle)
            mult = 1 if forward else -1
            dx = -math.sin(rad) * step * mult
            dy = -math.cos(rad) * step * mult
            new_x = int(round(x + dx))
            new_y = int(round(y + dy))
        except Exception:
            new_x, new_y = int(x), int(y)

        out_of_bounds = self.out_of_bounds(new_x, new_y)

        # anima para a nova posição calculada
        if not out_of_bounds:
            animate(actor, pos=(new_x, new_y), duration=0.1, tween='linear')

        if not bullet:
            # Som de movimento (nota curta) — respeita self.som quando actor for player ou bug
            try:
                if self.som:
                    tone.play('G3', 0.06)
            except Exception:
                pass

        return out_of_bounds

    def out_of_bounds(self, x, y, by = 0, bx = 0, w = 800, h = 600):
        if x < 0 + bx or x > w - bx or y < 50 + by or y > h - by:
            return True
        return False

    def actor_anime(self, actor: Actor):
        if not hasattr(actor, 'images'):
            return
        
        angle = actor.angle
        actor.image = actor.images[(actor.images.index(actor.image) + 1) % len(actor.images)] # algoritmo que verifica a imagem atual e determina a proxima com base na lista de imagems
        actor.angle = angle

    def key_down(self, keyboard, animate):
        if keyboard.m:
            # ativa/desativa o som
            self.som = not self.som
            try:
                if self.som:
                    self.play_theme()
                else:
                    self.stop_theme()
            except Exception:
                pass

        if self.state == 'intro':
            if keyboard.RETURN:
                # inicia o jogo
                self.state = 'game'
                self.players()
            if keyboard.Escape:
                # encerra o jogo
                sys.exit()

        elif self.state == 'game':
            if keyboard.Escape:
                self.state = 'intro'
                self.reset()
                self.start()
                return
            
            if keyboard.space:
                bullet = Actor('bullet-1', anchor=('center', 'center'))
                bullet.images = ['bullet-1', 'bullet-2', 'bullet-3']
                bullet.angle = self.player.angle
                bullet.x = self.player.x
                bullet.y = self.player.y
                self.objects.append(bullet)
                self.bullets.append(bullet)

                self.next_board(bullet, animate, True, True)

                # Som de disparo — respeita self.som
                try:
                    if self.som:
                        # som de disparo mais grave
                        tone.play('F#4', 0.08)
                except Exception:
                    pass

    def update(self, dt, keyboard, animate):
        if self.state != 'game':
            return

        if keyboard.left or keyboard.right or keyboard.up or keyboard.down:
            # use o valor acumulado do ângulo para permitir giros completos (>360)
            curr = self.player.angle

            new_angle = curr

            # right or left fica girando (agora em incrementos de 35°)
            if keyboard.right or keyboard.left:
                if keyboard.right:
                    new_angle = curr - 35
                elif keyboard.left:
                    new_angle = curr + 35

                animate(self.player, angle=new_angle, duration=0.1, tween='linear')

            elif keyboard.up or keyboard.down:
                self.next_board(self.player, animate, keyboard.up == True)

        if len(self.bugs) > 0 and (keyboard.left or keyboard.right or keyboard.up or keyboard.down or keyboard.space):
            bug = random.choice(self.bugs)

            # Calcula o vetor do bug até o player e obtém um ângulo que
            # segue a mesma convenção do jogador (0 = cima, aumenta CCW).
            vx = self.player.x - bug.x
            vy = self.player.y - bug.y
            angle = math.degrees(math.atan2(-vx, -vy)) % 360

            animate(bug, angle=angle, duration=0.1, tween='linear')
            # Move o bug um passo para frente nessa direção
            self.next_board(bug, animate, True)

        for bullet in self.bullets:
            self.next_board(bullet, animate, True, True)
            hasHit = False
            for bug in self.bugs:
                if bullet.colliderect(bug):
                    hasHit = True
                    self.objects.remove(bug)
                    self.bugs.remove(bug)
                    break

            if hasHit:
                self.objects.remove(bullet)
                self.bullets.remove(bullet)
                # Som de explosão quando um bug é acertado
                try:
                    if hasHit and self.som:
                        # explosão mais grave e longa
                        tone.play('C2', 0.20)
                        # nota de ressonância após 0.12s (grave)
                        tone.play('G2', 0.14)
                except Exception:
                    pass

    def draw(self, screen, keyboard, animate):
        screen.clear()

        for obj in self.objects:
            self.actor_anime(obj)
            obj.draw()

        if self.state == 'intro':
            screen.draw.text('Bem-vindo ao Battle Bugs!', center=(400, 50), color='white', fontsize=40)
            # adicione os controles e objetivos do jogo aqui
            screen.draw.text('Use as setas para mover e a barra de espaço para atirar', center=(400, 100), color='white', fontsize=40)
            self.player_image.draw()
            self.actor_anime(self.player_image)
            
            screen.draw.text('Dispare nos bugs!', center=(400, 200), color='white', fontsize=40)
            self.bug_image.draw()
            self.actor_anime(self.bug_image)

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
    battleBugs.key_down(keyboard, animate)

def update(dt):
    battleBugs.update(dt, keyboard, animate)

def draw():
    battleBugs.draw(screen, keyboard, animate)

pgzrun.go()