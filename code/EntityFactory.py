from code.Player import Player
from code.Enemy import Enemy
from code.Shot import Shot
from code.Container import Container
from code.Const import P_SHOT_DMG, P_SHOT_SPEED, E2_SHOT_DMG, E2_SHOT_SPEED


class EntityFactory:
    @staticmethod
    def create_player(x, y):
        return Player(x, y)

    @staticmethod
    def create_enemy(x, y, etype, facing_right=True):
        return Enemy(x, y, etype, facing_right)

    @staticmethod
    def create_player_shot(x, y, direction):
        return Shot(x, y, direction, "player", P_SHOT_DMG, P_SHOT_SPEED)

    @staticmethod
    def create_enemy_shot(x, y, direction):
        return Shot(x, y, direction, "enemy", E2_SHOT_DMG, E2_SHOT_SPEED)

    @staticmethod
    def create_container(x, y):
        return Container(x, y)
