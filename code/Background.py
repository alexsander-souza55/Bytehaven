import os
import pygame
from code.Const import WIDTH, HEIGHT

from code.Paths import BASE as _BASE

# Parallax speeds per layer (fraction of camera movement)
_SPEEDS = [0.1, 0.3, 0.5]


class Background:
    def __init__(self):
        self.layers = []
        for i, speed in enumerate(_SPEEDS):
            path = os.path.join(_BASE, "asset", "sprites", f"bg_layer{i}.png")
            try:
                img = pygame.image.load(path).convert_alpha()
                img = pygame.transform.scale(img, (WIDTH, HEIGHT))
            except Exception:
                img = pygame.Surface((WIDTH, HEIGHT))
                img.fill((5 + i * 4, 5 + i * 4, 15 + i * 6))
            self.layers.append({"img": img, "speed": speed})

    def draw(self, surface, cam_x):
        for layer in self.layers:
            offset = int(cam_x * layer["speed"]) % WIDTH
            surface.blit(layer["img"], (-offset, 0))
            surface.blit(layer["img"], (WIDTH - offset, 0))
