import pygame
from abc import ABC, abstractmethod


class Entity(ABC):
    def __init__(self, x, y, w, h, hp, score_value=0):
        self.x = float(x)
        self.y = float(y)
        self.w = w
        self.h = h
        self.hp = hp
        self.max_hp = hp
        self.score_value = score_value
        self.alive = True
        self.vel_x = 0.0
        self.vel_y = 0.0

        self.frames = {}
        self.current_anim = "idle"
        self.frame_index = 0
        self.anim_timer = 0
        self.anim_speed = 6
        self.facing_right = True

    def load_sheet(self, path, frame_w, frame_h, scale=1):
        sheet = pygame.image.load(path).convert_alpha()
        n = sheet.get_width() // frame_w
        result = []
        for i in range(n):
            f = sheet.subsurface((i * frame_w, 0, frame_w, frame_h))
            if scale != 1:
                f = pygame.transform.scale(f, (frame_w * scale, frame_h * scale))
            result.append(f)
        return result

    def set_anim(self, name):
        if name != self.current_anim:
            self.current_anim = name
            self.frame_index = 0
            self.anim_timer = 0

    def tick_anim(self):
        frames = self.frames.get(self.current_anim)
        if not frames:
            return
        self.anim_timer += 1
        if self.anim_timer >= self.anim_speed:
            self.anim_timer = 0
            self.frame_index = (self.frame_index + 1) % len(frames)

    def get_rect(self):
        return pygame.Rect(int(self.x), int(self.y), self.w, self.h)

    def take_damage(self, amount):
        self.hp = max(0, self.hp - amount)
        if self.hp == 0:
            self.alive = False

    def blit(self, surface, cam_x):
        frames = self.frames.get(self.current_anim)
        if not frames:
            return
        frame = frames[self.frame_index % len(frames)]
        if not self.facing_right:
            frame = pygame.transform.flip(frame, True, False)
        surface.blit(frame, (int(self.x) - cam_x, int(self.y)))

    @abstractmethod
    def update(self, *args, **kwargs):
        pass

    @abstractmethod
    def draw(self, surface, cam_x):
        pass
