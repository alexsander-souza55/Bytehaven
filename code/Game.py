import os
import sys
import pygame
from code.Const import *
from code.Menu import Menu
from code.Level import Level
from code.Score import Score
import code.SoundFX as SoundFX

_BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(TITLE)
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock  = pygame.time.Clock()

        self.state      = ST_MENU
        self.menu       = Menu(self.screen)
        self.level      = None
        self.score_scr  = None
        self.level1_score = 0
        self._init_audio()

    # ------------------------------------------------------------------ audio
    def _init_audio(self):
        try:
            pygame.mixer.init()
            SoundFX.init()
        except Exception:
            pass

    def _play(self, name):
        path = os.path.join(_BASE, "asset", "audio", name)
        try:
            if os.path.isfile(path):
                pygame.mixer.music.load(path)
                pygame.mixer.music.play(-1)
        except Exception:
            pass

    # ------------------------------------------------------------------ main loop
    def run(self):
        self._play("menu.mp3")

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    if self.state not in (ST_MENU,):
                        self.state = ST_MENU
                        self.menu  = Menu(self.screen)
                        self._play("menu.mp3")
                        continue

                if self.state == ST_MENU:
                    choice = self.menu.handle(event)
                    if choice == 0:
                        self._start_level(1)
                    elif choice == 1:
                        pygame.quit()
                        sys.exit()

                elif self.state in (ST_VICTORY, ST_LOSE):
                    result = self.score_scr.handle(event)
                    if result == "menu":
                        self.state = ST_MENU
                        self.menu  = Menu(self.screen)
                        self._play("menu.mp3")

            # -------------------------------------------------------------- update
            if self.state in (ST_LEVEL1, ST_LEVEL2):
                keys   = pygame.key.get_pressed()
                result = self.level.update(keys)

                if result == "win":
                    if self.level.num == 1:
                        self.level1_score = self.level.score
                        self._start_level(2)
                    else:
                        final = self.level1_score + self.level.score
                        self._end_game(final, "win")

                elif result == "lose":
                    final = self.level1_score + self.level.score
                    self._end_game(final, "lose")

            # -------------------------------------------------------------- draw
            if self.state == ST_MENU:
                self.menu.draw()
            elif self.state in (ST_LEVEL1, ST_LEVEL2):
                self.level.draw()
            elif self.state in (ST_VICTORY, ST_LOSE):
                self.score_scr.draw()

            pygame.display.flip()
            self.clock.tick(FPS)

    # ------------------------------------------------------------------ helpers
    def _start_level(self, num):
        self.level = Level(num, self.screen)
        self.state = ST_LEVEL1 if num == 1 else ST_LEVEL2
        self._play(f"level{num}.mp3")

    def _end_game(self, score, result):
        self.state     = ST_VICTORY if result == "win" else ST_LOSE
        self.score_scr = Score(self.screen, score, result)
        if result == "win":
            self._play("victory.mp3")
        else:
            try:
                pygame.mixer.music.stop()
            except Exception:
                pass
