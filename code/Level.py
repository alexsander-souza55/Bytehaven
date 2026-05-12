import os
import pygame
from code.Const import *
from code.Background import Background
from code.EntityFactory import EntityFactory
from code.EntityMediator import EntityMediator
from code.Shot import Shot
import code.SoundFX as SoundFX

_BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# fmt: (x, y, tiles_wide)
_LEVELS = {
    1: {
        "world_w": 3200,
        "platforms": [
            (288,  320, 4), (608,  260, 5), (896,  300, 4),
            (1120, 220, 6), (1408, 280, 4), (1696, 240, 5),
            (2016, 300, 4), (2304, 200, 6), (2592, 280, 4),
            (2880, 260, 5),
        ],
        # (x, platform_y)  — container sits on top of that platform
        "containers": [(672, 260), (1312, 220), (2112, 300)],
        # (etype, x, platform_y)
        "enemies": [
            (1, 350,  320), (1, 1180, 220), (1, 1760, 240),
            (2, 2380, 200), (2, 2944, 260),
        ],
        "exit_x": 3060,
    },
    2: {
        "world_w": 3200,
        "platforms": [
            (224,  340, 3), (512,  280, 3), (768,  200, 4),
            (1024, 280, 3), (1280, 180, 5), (1568, 260, 3),
            (1824, 200, 4), (2080, 280, 3), (2336, 160, 6),
            (2656, 240, 4), (2944, 280, 3),
        ],
        "containers": [(800, 200), (1728, 200), (2656, 240)],
        "enemies": [
            (1, 400,  340), (2, 900,  200), (1, 1568, 260),
            (2, 2080, 280), (1, 2500, 160), (2, 2944, 280),
        ],
        "exit_x": 3060,
    },
}


class Level:
    def __init__(self, num, screen):
        self.num    = num
        self.screen = screen
        self.data   = _LEVELS[num]
        self.world_w  = self.data["world_w"]
        self.ground_y = HEIGHT - TILE   # 418
        self.cam_x    = 0
        self.score    = 0
        self.result   = None   # "win" | "lose"

        self._load_tiles()
        self.platforms  = self._build_platforms()
        self.player     = self._spawn_player()
        self.enemies    = self._spawn_enemies()
        self.containers = self._spawn_containers()
        self.shots      = []
        self.bg         = Background()

        self.exit_rect     = pygame.Rect(self.data["exit_x"],
                                         self.ground_y - 80, 48, 80)
        self.exit_unlocked = False
        self._font    = pygame.font.SysFont("monospace", 15)
        self._font_sm = pygame.font.SysFont("monospace", 12)

    # ------------------------------------------------------------------ setup
    def _load_tiles(self):
        def load(name, fallback_color):
            path = os.path.join(_BASE, "asset", "sprites", name)
            try:
                img = pygame.image.load(path).convert_alpha()
                return pygame.transform.scale(img, (TILE, TILE))
            except Exception:
                s = pygame.Surface((TILE, TILE))
                s.fill(fallback_color)
                return s

        self.t_ground    = load("tile_ground.png",    (20, 20, 50))
        self.t_platform  = load("tile_platform.png",  (30, 60, 80))
        self.t_corrupted = load("tile_corrupted.png", (80, 10, 10))

    def _build_platforms(self):
        rects = []
        n_ground = self.world_w // TILE + 1
        for i in range(n_ground):
            rects.append(pygame.Rect(i * TILE, self.ground_y, TILE, TILE))
        for px, py, tiles in self.data["platforms"]:
            for i in range(tiles):
                rects.append(pygame.Rect(px + i * TILE, py, TILE, TILE))
        return rects

    def _spawn_player(self):
        ph = P_FRAME * P_SCALE
        return EntityFactory.create_player(100, self.ground_y - ph)

    def _spawn_enemies(self):
        eh = E1_FRAME * E1_SCALE
        enemies = []
        for etype, ex, plat_y in self.data["enemies"]:
            enemies.append(EntityFactory.create_enemy(ex, plat_y - eh, etype))
        return enemies

    def _spawn_containers(self):
        containers = []
        for cx, plat_y in self.data["containers"]:
            containers.append(EntityFactory.create_container(cx, plat_y - CONT_H))
        return containers

    # ------------------------------------------------------------------ update
    def update(self, keys):
        if self.result:
            return self.result

        # Player
        shot_data = self.player.update(keys, self.platforms, self.world_w)
        if shot_data:
            _, sx, sy, sd = shot_data
            self.shots.append(EntityFactory.create_player_shot(sx, sy, sd))

        # Enemies
        for enemy in self.enemies:
            shot_data = enemy.update(self.platforms, self.world_w, self.player.x)
            if shot_data:
                _, sx, sy, sd = shot_data
                self.shots.append(EntityFactory.create_enemy_shot(sx, sy, sd))

        # Purge finished death animations
        self.enemies = [e for e in self.enemies if not e.death_done]

        # Shots
        for shot in self.shots:
            shot.update(self.world_w)
        self.shots = [s for s in self.shots if s.alive]

        # Containers animation
        for c in self.containers:
            c.update()

        # Mediator
        self.score += EntityMediator.player_shots_vs_enemies(self.shots, self.enemies)
        EntityMediator.enemy_shots_vs_player(self.shots, self.player)
        EntityMediator.enemies_vs_player(self.enemies, self.player)
        gained = EntityMediator.containers_vs_player(self.containers, self.player)
        if gained:
            SoundFX.play("collect")
        self.player.containers += gained
        EntityMediator.corrupted_zone(self.player, self.ground_y + TILE)

        # Exit unlock
        if self.player.containers >= CONTAINERS_PER_LEVEL:
            self.exit_unlocked = True

        # Win check
        if (self.exit_unlocked and
                self.player.get_rect().colliderect(self.exit_rect)):
            self.result = "win"

        # Lose check
        if self.player.dying and self.player.death_done:
            self.result = "lose"

        # Camera
        target = int(self.player.x + self.player.w / 2 - WIDTH / 2)
        self.cam_x = max(0, min(target, self.world_w - WIDTH))

        return None

    # ------------------------------------------------------------------ draw
    def draw(self):
        self.screen.fill(DARK_BG)
        self.bg.draw(self.screen, self.cam_x)
        self._draw_tiles()
        self._draw_corrupted_strip()
        for c in self.containers:
            c.draw(self.screen, self.cam_x)
        self._draw_exit()
        for enemy in self.enemies:
            enemy.draw(self.screen, self.cam_x)
        for shot in self.shots:
            shot.draw(self.screen, self.cam_x)
        self.player.draw(self.screen, self.cam_x)
        self._draw_hud()

    def _draw_tiles(self):
        # Ground
        n = self.world_w // TILE + 1
        for i in range(n):
            tx = i * TILE - self.cam_x
            if -TILE <= tx <= WIDTH + TILE:
                self.screen.blit(self.t_ground, (tx, self.ground_y))
        # Floating platforms
        for px, py, tiles in self.data["platforms"]:
            for i in range(tiles):
                tx = px + i * TILE - self.cam_x
                if -TILE <= tx <= WIDTH + TILE:
                    self.screen.blit(self.t_platform, (tx, py))

    def _draw_corrupted_strip(self):
        n = WIDTH // TILE + 2
        for i in range(n):
            self.screen.blit(self.t_corrupted, (i * TILE, HEIGHT - TILE))

    def _draw_exit(self):
        ex = self.data["exit_x"] - self.cam_x
        color = CYAN if self.exit_unlocked else (40, 40, 90)
        pygame.draw.rect(self.screen, color,
                         (ex, self.exit_rect.y, self.exit_rect.w, self.exit_rect.h), 3)
        label = self._font_sm.render(
            "EXIT" if self.exit_unlocked else "LOCKED", True, color)
        self.screen.blit(label, (ex + self.exit_rect.w // 2 - label.get_width() // 2,
                                 self.exit_rect.y - 16))

    def _draw_hud(self):
        # Container counter (top centre)
        total = CONTAINERS_PER_LEVEL
        got   = self.player.containers
        ct = self._font.render(f"CONTAINERS: {got}/{total}", True, CYAN)
        self.screen.blit(ct, (WIDTH // 2 - ct.get_width() // 2, 10))

        # Score (top right)
        sc = self._font.render(f"SCORE: {self.score}", True, WHITE)
        self.screen.blit(sc, (WIDTH - sc.get_width() - 10, 10))

        # Level (below container counter)
        lv = self._font_sm.render(f"LEVEL {self.num}", True, PURPLE)
        self.screen.blit(lv, (WIDTH // 2 - lv.get_width() // 2, 28))

        # HP label (next to bar)
        hp_lbl = self._font_sm.render(
            f"HP: {self.player.hp}/{self.player.max_hp}", True, WHITE)
        self.screen.blit(hp_lbl, (10, 24))

        # ESC hint
        esc = self._font_sm.render("ESC — menu", True, (60, 60, 100))
        self.screen.blit(esc, (WIDTH - esc.get_width() - 8, HEIGHT - 18))
