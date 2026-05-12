import os
import random
import pygame
from code.Entity import Entity
from code.Const import *
import code.SoundFX as SoundFX

_BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class Enemy(Entity):
    def __init__(self, x, y, etype, facing_right=True):
        self.etype = etype
        if etype == 1:
            hp, spd, score = E1_HP, E1_SPEED, E1_SCORE
            self.contact_dmg = E1_DMG
            self.can_shoot   = False
        else:
            hp, spd, score = E2_HP, E2_SPEED, E2_SCORE
            self.contact_dmg = E2_DMG
            self.can_shoot   = True

        w = E1_FRAME * E1_SCALE
        h = E1_FRAME * E1_SCALE
        super().__init__(x, y, w, h, hp, score)
        self.facing_right = facing_right
        self.vel_x        = spd * (1 if facing_right else -1)
        self.shoot_timer  = random.randint(0, E2_SHOT_DELAY)
        self.hurt_timer   = 0
        self.dying        = False
        self.death_done   = False
        self._load_sprites()

    def _load_sprites(self):
        if self.etype == 1:
            folder = os.path.join(_BASE, "asset", "sprites",
                                  "Free 3 Cyberpunk Sprites Pixel Art", "1 Biker")
            px = "Biker"
            sc = E1_SCALE
        else:
            folder = os.path.join(_BASE, "asset", "sprites",
                                  "Free 3 Cyberpunk Sprites Pixel Art", "2 Punk")
            px = "Punk"
            sc = E2_SCALE

        def s(name):
            try:
                return self.load_sheet(os.path.join(folder, name),
                                       E1_FRAME, E1_FRAME, sc)
            except Exception:
                surf = pygame.Surface((E1_FRAME * sc, E1_FRAME * sc),
                                      pygame.SRCALPHA)
                color = RED if self.etype == 1 else PURPLE
                pygame.draw.rect(surf, color, surf.get_rect().inflate(-8, -8), 2)
                return [surf]

        self.frames = {
            "run":   s(f"{px}_run.png"),
            "idle":  s(f"{px}_idle.png"),
            "hurt":  s(f"{px}_hurt.png"),
            "death": s(f"{px}_death.png"),
        }

    # ------------------------------------------------------------------
    def update(self, platforms, world_w, player_x=None):
        if self.dying:
            self.tick_anim()
            death_frames = self.frames.get("death", [])
            if death_frames and self.frame_index >= len(death_frames) - 1:
                self.death_done = True
            return None

        if self.hurt_timer > 0:
            self.hurt_timer -= 1

        # Horizontal
        self.x += self.vel_x
        self.x = max(0.0, min(self.x, float(world_w - self.w)))
        if self.x <= 0 or self.x >= world_w - self.w:
            self._flip()

        # Gravity + vertical
        self.vel_y = min(self.vel_y + GRAVITY, MAX_FALL)
        self.y += self.vel_y

        # Platform collision
        on_ground = False
        er = self.get_rect()
        for plat in platforms:
            if er.colliderect(plat) and self.vel_y > 0:
                self.y = float(plat.top - self.h)
                self.vel_y = 0.0
                on_ground = True
                er = self.get_rect()
                break

        # Edge detection — reverse if about to walk off platform
        if on_ground and self.vel_x != 0:
            er = self.get_rect()
            if self.vel_x > 0:
                probe = pygame.Rect(er.right + 2, er.bottom + 2, 4, 4)
            else:
                probe = pygame.Rect(er.left - 6, er.bottom + 2, 4, 4)
            if not any(probe.colliderect(p) for p in platforms):
                self._flip()

        # Animation
        if self.hurt_timer > 0:
            self.set_anim("hurt")
        else:
            self.set_anim("run")
        self.tick_anim()

        # Shoot (Enemy 2 only)
        shot = None
        if self.can_shoot and player_x is not None:
            self.shoot_timer -= 1
            if self.shoot_timer <= 0:
                self.shoot_timer = E2_SHOT_DELAY
                direction = 1 if player_x > self.x else -1
                sx = self.x + self.w if direction > 0 else self.x
                shot = ("enemy", sx, self.y + self.h * 0.45, direction)
        return shot

    def _flip(self):
        self.vel_x = -self.vel_x
        self.facing_right = self.vel_x > 0

    def take_damage(self, amount):
        if self.hurt_timer > 0:
            return
        super().take_damage(amount)
        self.hurt_timer = 20
        if self.hp == 0:
            self.dying = True
            self.set_anim("death")
            SoundFX.play("enemy_death")

    def draw(self, surface, cam_x):
        self.blit(surface, cam_x)
