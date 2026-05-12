import os
import pygame
from code.Const import CYAN, WHITE, CONT_W, CONT_H

from code.Paths import BASE as _BASE

_W = CONT_W * 2   # 64 px (2× scale)
_H = CONT_H       # 48 px


class Container:
    def __init__(self, x, y):
        self.x         = x
        self.y         = y
        self.w         = _W
        self.h         = _H
        self.collected = False
        self.timer     = 0
        self.frame     = 0
        self.frames    = self._load()

    def _load(self):
        path = os.path.join(_BASE, "asset", "sprites", "container.png")
        try:
            sheet = pygame.image.load(path).convert_alpha()
            fw = sheet.get_width() // 2
            fh = sheet.get_height()
            frames = []
            for i in range(2):
                f = sheet.subsurface((i * fw, 0, fw, fh))
                frames.append(pygame.transform.scale(f, (_W, _H)))
            return frames
        except Exception:
            surf = pygame.Surface((_W, _H), pygame.SRCALPHA)
            pygame.draw.rect(surf, CYAN, surf.get_rect().inflate(-6, -6), 2)
            pygame.draw.circle(surf, CYAN, (_W // 2, _H // 2), 10)
            return [surf, surf]

    def update(self):
        self.timer += 1
        if self.timer >= 25:
            self.timer = 0
            self.frame = (self.frame + 1) % len(self.frames)

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.w, self.h)

    def draw(self, surface, cam_x):
        if self.collected:
            return
        surface.blit(self.frames[self.frame], (self.x - cam_x, self.y))
        # Label above container
        font = pygame.font.SysFont("monospace", 11)
        label = font.render("CONTAINER", True, CYAN)
        surface.blit(label, (self.x - cam_x + self.w // 2 - label.get_width() // 2,
                             self.y - 14))
