import os
import pygame
from code.Entity import Entity
from code.Const import *
import code.SoundFX as SoundFX

from code.Paths import BASE as _BASE
_MAIN = os.path.join(_BASE, "asset", "sprites",
                     "Free 3 Cyberpunk Sprites Pixel Art", "3 Cyborg")


class Player(Entity):
    def __init__(self, x, y):
        w = P_FRAME * P_SCALE
        h = P_FRAME * P_SCALE
        super().__init__(x, y, w, h, P_HP)
        self._load_sprites()
        self.on_ground   = False
        self.shot_timer  = 0
        self.hurt_timer  = 0
        self.score       = 0
        self.containers  = 0
        self.dying       = False
        self.death_done  = False

    def _load_sprites(self):
        def s(name):
            try:
                return self.load_sheet(os.path.join(_MAIN, name),
                                       P_FRAME, P_FRAME, P_SCALE)
            except Exception:
                surf = pygame.Surface((P_FRAME * P_SCALE, P_FRAME * P_SCALE),
                                      pygame.SRCALPHA)
                pygame.draw.rect(surf, CYAN,
                                 surf.get_rect().inflate(-8, -8), 2)
                return [surf]

        self.frames = {
            "idle":   s("Cyborg_idle.png"),
            "run":    s("Cyborg_run.png"),
            "jump":   s("Cyborg_jump.png"),
            "attack": s("Cyborg_attack1.png"),
            "hurt":   s("Cyborg_hurt.png"),
            "death":  s("Cyborg_death.png"),
        }

    # ------------------------------------------------------------------
    def update(self, keys, platforms, world_w):
        if self.dying:
            self.tick_anim()
            death_frames = self.frames.get("death", [])
            if death_frames and self.frame_index >= len(death_frames) - 1:
                self.death_done = True
            return None

        moving = False
        if keys[pygame.K_a]:
            self.vel_x = -P_SPEED
            self.facing_right = False
            moving = True
        elif keys[pygame.K_d]:
            self.vel_x = P_SPEED
            self.facing_right = True
            moving = True
        else:
            self.vel_x = 0

        if (keys[pygame.K_w] or keys[pygame.K_SPACE]) and self.on_ground:
            self.vel_y = P_JUMP
            self.on_ground = False
            SoundFX.play("jump")

        prev_bottom = self.y + self.h

        # Gravity + move
        self.vel_y = min(self.vel_y + GRAVITY, MAX_FALL)
        self.x += self.vel_x
        self.x = max(0.0, min(self.x, float(world_w - self.w)))
        self.y += self.vel_y

        # Platform collision — só resolve em Y se o jogador estava acima da plataforma
        self.on_ground = False
        pr = self.get_rect()
        for plat in platforms:
            if pr.colliderect(plat):
                if self.vel_y > 0 and prev_bottom <= plat.top + 4:
                    self.y = float(plat.top - self.h)
                    self.vel_y = 0.0
                    self.on_ground = True
                elif self.vel_y < 0:
                    self.y = float(plat.bottom)
                    self.vel_y = 0.0
                pr = self.get_rect()

        # Shoot
        shot = None
        self.shot_timer = max(0, self.shot_timer - 1)
        if (keys[pygame.K_LCTRL] or keys[pygame.K_RCTRL]) and self.shot_timer == 0:
            self.shot_timer = P_SHOT_DELAY
            sx = self.x + self.w if self.facing_right else self.x
            shot = ("player", sx, self.y + self.h * 0.45,
                    1 if self.facing_right else -1)
            SoundFX.play("shoot")

        if self.hurt_timer > 0:
            self.hurt_timer -= 1

        self._pick_anim(moving)
        self.tick_anim()
        return shot

    def _pick_anim(self, moving):
        if self.hurt_timer > P_HURT_FRAMES - 10:
            self.set_anim("hurt")
        elif not self.on_ground:
            self.set_anim("jump")
        elif self.shot_timer > P_SHOT_DELAY - 8:
            self.set_anim("attack")
        elif moving:
            self.set_anim("run")
        else:
            self.set_anim("idle")

    def take_damage(self, amount):
        if self.hurt_timer > 0:
            return
        super().take_damage(amount)
        self.hurt_timer = P_HURT_FRAMES
        SoundFX.play("hurt")
        if self.hp == 0:
            self.dying = True
            self.set_anim("death")

    # ------------------------------------------------------------------
    def draw(self, surface, cam_x):
        # Blink when hurt
        if self.hurt_timer > 0 and (self.hurt_timer // 4) % 2 == 1:
            return
        self.blit(surface, cam_x)
        self._draw_hp(surface)

    def _draw_hp(self, surface):
        bw, bh = 200, 12
        x, y = 10, 10
        ratio = self.hp / self.max_hp
        pygame.draw.rect(surface, (80, 0, 0), (x, y, bw, bh))
        pygame.draw.rect(surface, CYAN,       (x, y, int(bw * ratio), bh))
        pygame.draw.rect(surface, WHITE,      (x, y, bw, bh), 2)
