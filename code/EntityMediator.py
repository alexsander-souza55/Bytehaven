class EntityMediator:

    @staticmethod
    def player_shots_vs_enemies(shots, enemies):
        score = 0
        for shot in shots:
            if shot.owner != "player" or not shot.alive:
                continue
            sr = shot.get_rect()
            for enemy in enemies:
                if enemy.dying:
                    continue
                if sr.colliderect(enemy.get_rect()):
                    enemy.take_damage(shot.damage)
                    shot.alive = False
                    if enemy.dying:
                        score += enemy.score_value
                    break
        return score

    @staticmethod
    def enemy_shots_vs_player(shots, player):
        for shot in shots:
            if shot.owner != "enemy" or not shot.alive:
                continue
            if shot.get_rect().colliderect(player.get_rect()):
                player.take_damage(shot.damage)
                shot.alive = False

    @staticmethod
    def enemies_vs_player(enemies, player):
        for enemy in enemies:
            if enemy.dying:
                continue
            if enemy.get_rect().colliderect(player.get_rect()):
                player.take_damage(enemy.contact_dmg)

    @staticmethod
    def containers_vs_player(containers, player):
        collected = 0
        for c in containers:
            if not c.collected and c.get_rect().colliderect(player.get_rect()):
                c.collected = True
                collected += 1
        return collected

    @staticmethod
    def corrupted_zone(player, zone_y):
        if player.y + player.h >= zone_y:
            player.hp = 0
            player.dying = True
            player.set_anim("death")
