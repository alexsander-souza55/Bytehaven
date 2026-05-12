import os
import pygame
from code.Const import *

_BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class Menu:
    _OPTIONS = ["INICIAR JOGO", "SAIR"]

    def __init__(self, screen):
        self.screen   = screen
        self.selected = 0
        self._ft  = pygame.font.SysFont("monospace", 38, bold=True)
        self._fs  = pygame.font.SysFont("monospace", 20)
        self._fc  = pygame.font.SysFont("monospace", 14)
        self._bg  = self._load_bg()

    def _load_bg(self):
        path = os.path.join(_BASE, "asset", "sprites", "menu_bg.png")
        try:
            img = pygame.image.load(path).convert()
            return pygame.transform.scale(img, (WIDTH, HEIGHT))
        except Exception:
            s = pygame.Surface((WIDTH, HEIGHT))
            s.fill(DARK_BG)
            return s

    # ------------------------------------------------------------------
    def handle(self, event):
        if event.type != pygame.KEYDOWN:
            return None
        if event.key in (pygame.K_w, pygame.K_UP):
            self.selected = (self.selected - 1) % len(self._OPTIONS)
        elif event.key in (pygame.K_s, pygame.K_DOWN):
            self.selected = (self.selected + 1) % len(self._OPTIONS)
        elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
            return self.selected
        return None

    def draw(self):
        self.screen.blit(self._bg, (0, 0))

        # Title
        t1 = self._ft.render("BYTEHAVEN", True, CYAN)
        t2 = self._fs.render("THE LOST CONTAINERS", True, PURPLE)
        self.screen.blit(t1, (WIDTH // 2 - t1.get_width() // 2, 50))
        self.screen.blit(t2, (WIDTH // 2 - t2.get_width() // 2, 98))

        # Options
        for i, opt in enumerate(self._OPTIONS):
            color  = CYAN if i == self.selected else WHITE
            prefix = "> " if i == self.selected else "  "
            surf = self._fs.render(prefix + opt, True, color)
            self.screen.blit(surf, (WIDTH // 2 - surf.get_width() // 2,
                                    195 + i * 42))

        # Controls box
        self._draw_controls()

        # Footer
        f = self._fc.render("W/S: navegar   ENTER: confirmar", True, (70, 70, 110))
        self.screen.blit(f, (WIDTH // 2 - f.get_width() // 2, HEIGHT - 22))

    def _draw_controls(self):
        box_x, box_y = WIDTH // 2 - 145, 300
        box_w, box_h = 290, 110
        pygame.draw.rect(self.screen, (10, 10, 30), (box_x, box_y, box_w, box_h))
        pygame.draw.rect(self.screen, PURPLE,        (box_x, box_y, box_w, box_h), 1)

        hdr = self._fc.render("— CONTROLES —", True, PURPLE)
        self.screen.blit(hdr, (WIDTH // 2 - hdr.get_width() // 2, box_y + 8))

        for i, line in enumerate(CONTROLS):
            surf = self._fc.render(line, True, (180, 180, 220))
            self.screen.blit(surf, (WIDTH // 2 - surf.get_width() // 2,
                                    box_y + 28 + i * 18))
