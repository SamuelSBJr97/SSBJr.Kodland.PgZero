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

        self.bugs = []
        self.bullets = []

        self.board: Actor
        self.player: Actor

        self.bug_image: Actor
        self.player_image: Actor

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

        self.player = Actor("player-1", anchor=('center', 'center'))
        self.player.images = ['player-1', 'player-2', 'player-3', 'player-4']
        self.player.angle = 0

        self.reset()
        self.start()

    def reset(self):
        self.clear()
        self.state = 'intro'  # intro, start, gameover

    def clear(self):
        self.bugs.clear()
        self.bullets.clear()

    def start(self):
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
        self.bugs.clear()
        for _ in range(5):
            bug = Actor('bug-1', anchor=('center', 'center'))
            bug.images = ['bug-1', 'bug-2', 'bug-3', 'bug-4']
            bug.angle = 0

            bug.x = random.randint(1, 7) * 50
            bug.y = random.randint(1, 9) * 50 + 50
            self.bugs.append(bug)

        self.player.x = random.randint(1, 7) * 50
        self.player.y = random.randint(1, 9) * 50 + 50

    def next_board(self, actor, animate, forward=True, rotate=False, new_angle=0.0, bullet=False):

        if rotate:
            # gira o ator 35 graus na direção desejada
            animate(actor, angle=new_angle, duration=0.1, tween='linear')
            return False
        
        x = actor.x
        y = actor.y

        step = 50

        if bullet:
            step = 100

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

        if bullet:
            has_hit = None

            # se sair dos limites, remove a bala
            animate(actor, pos=(new_x, new_y), duration=0.1, tween='linear', on_finished=lambda: self.bullet_collide(actor, bug=has_hit) if out_of_bounds else None)
            
            if actor.shooter == 'player':
                for bug in self.bugs:
                    if bug.colliderect(actor):
                        has_hit = bug
                        break
            elif actor.shooter == 'bug':
                if self.player.colliderect(actor):
                    has_hit = self.player

            if has_hit:
                self.bullet_collide(actor, bug=has_hit, player=self.player if has_hit == self.player else None)

        elif not bullet:
            if not out_of_bounds:
                animate(actor, pos=(new_x, new_y), duration=0.1, tween='linear')

            # Som de movimento (nota curta) — respeita self.som quando actor for player ou bug
            try:
                if self.som:
                    tone.play('G3', 0.06)
            except Exception:
                pass

        return out_of_bounds

    def bullet_collide(self, bullet, bug=None, player=None):
        # Som de explosão quando um bug é acertado
        try:
            if self.som:
                # explosão mais grave e longa
                tone.play('C2', 0.20)
                # nota de ressonância após 0.12s (grave)
                tone.play('G2', 0.14)
        except Exception:
            pass

        if player:
            self.state = 'gameover'
        else:
            if bullet in self.bullets:
                self.bullets.remove(bullet)
            if bug and bug in self.bugs:
                self.bugs.remove(bug)

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

        elif self.state == 'game' or self.state == 'gameover':
            if keyboard.RETURN:
                # inicia o jogo
                self.state = 'game'
                self.players()
                return
            
            if keyboard.Escape:
                # volta ao intro
                self.state = 'intro'
                self.reset()
                self.start()
                return
            
            if self.state == 'game':
                if keyboard.space:
                    bullet = Actor('bullet-1', anchor=('center', 'center'))
                    bullet.images = ['bullet-1', 'bullet-2', 'bullet-3']
                    bullet.angle = self.player.angle
                    bullet.x = self.player.x
                    bullet.y = self.player.y
                    bullet.shooter = 'player'
                    self.bullets.append(bullet)

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

                self.next_board(self.player, animate, rotate=True, new_angle=new_angle)

            elif keyboard.up or keyboard.down:
                self.next_board(self.player, animate, forward=keyboard.up == True)

        if len(self.bugs) > 0 and (keyboard.left or keyboard.right or keyboard.up or keyboard.down or keyboard.space):
            bug = random.choice(self.bugs)

            # Calcula o vetor do bug até o player e obtém um ângulo que
            # segue a mesma convenção do jogador (0 = cima, aumenta CCW).
            vx = self.player.x - bug.x
            vy = self.player.y - bug.y
            angle = math.degrees(math.atan2(-vx, -vy)) % 360

            self.next_board(bug, animate, rotate=True, new_angle=angle)
            # Move o bug um passo para frente nessa direção
            self.next_board(bug, animate, forward=True)

            if random.random() < 0.1 and keyboard.space:  # 10% de chance de atirar se o jogador atirar
                bullet = Actor('bullet-1', anchor=('center', 'center'))
                bullet.images = ['bullet-1', 'bullet-2', 'bullet-3']
                bullet.angle = bug.angle
                bullet.x = bug.x
                bullet.y = bug.y
                bullet.shooter = 'bug'
                self.bullets.append(bullet)

                # Som de disparo do bug — respeita self.som
                try:
                    if self.som:
                        # som de disparo mais agudo para o bug
                        tone.play('A4', 0.08)
                except Exception:
                    pass

        for bullet in self.bullets:
            self.next_board(bullet, animate, forward=True, bullet=True)

    def draw(self, screen, keyboard, animate):
        screen.clear()

        if self.state == 'intro':
            for obj in [self.board]:
                self.actor_anime(obj)
                obj.draw()

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

        if self.state == 'game' or self.state == 'gameover':
            for obj in [self.board, self.player, *self.bugs, *self.bullets]:
                self.actor_anime(obj)
                obj.draw()

            if len(self.bugs) == 0:
                screen.draw.text('Parabéns! Você venceu!', center=(400, 250), color='white', fontsize=40)
                screen.draw.text('Tecle Enter para reiniciar', center=(400, 300), color='white', fontsize=40)
                screen.draw.text('Tecle Esc para ir ao menu', center=(400, 350), color='white', fontsize=40)
                self.clear()
            elif self.state == 'gameover':
                screen.draw.text('Game Over! Você foi atingido!', center=(400, 250), color='white', fontsize=40)
                screen.draw.text('Tecle Enter para reiniciar', center=(400, 300), color='white', fontsize=40)
                screen.draw.text('Tecle Esc para ir ao menu', center=(400, 350), color='white', fontsize=40)

            if len(self.bugs) > 0:
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