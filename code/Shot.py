import os
import pygame
from code.Const import CYAN, RED

_BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_BULLETS = os.path.join(_BASE, "asset", "sprites",
                         "free-guns-for-cyberpunk-characters-pixel-art",
                         "5 Bullets")


class Shot:
    W = 18
    H = 8

    def __init__(self, x, y, direction, owner, damage, speed):
        self.x         = float(x)
        self.y         = float(y)
        self.direction = direction
        self.owner     = owner
        self.damage    = damage
        self.speed     = speed
        self.alive     = True
        self.image     = self._load()

    def _load(self):
        fname = "1.png" if self.owner == "player" else "3.png"
        try:
            img = pygame.image.load(os.path.join(_BULLETS, fname)).convert_alpha()
            img = pygame.transform.scale(img, (self.W, self.H))
        except Exception:
            img = pygame.Surface((self.W, self.H), pygame.SRCALPHA)
            color = CYAN if self.owner == "player" else RED
            pygame.draw.ellipse(img, color, img.get_rect())
        if self.direction < 0:
            img = pygame.transform.flip(img, True, False)
        return img

    def update(self, world_w):
        self.x += self.speed * self.direction
        if self.x < -self.W or self.x > world_w + self.W:
            self.alive = False

    def get_rect(self):
        return pygame.Rect(int(self.x), int(self.y), self.W, self.H)

    def draw(self, surface, cam_x):
        surface.blit(self.image, (int(self.x) - cam_x, int(self.y)))
