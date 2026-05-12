import os
import pygame

from code.Paths import BASE as _BASE
_sounds = {}


def init():
    for name in ("shoot", "jump", "collect", "hurt", "enemy_death"):
        path = os.path.join(_BASE, "asset", "audio", f"{name}.wav")
        try:
            snd = pygame.mixer.Sound(path)
            snd.set_volume(0.5)
            _sounds[name] = snd
        except Exception:
            pass


def play(name):
    s = _sounds.get(name)
    if s:
        s.play()
