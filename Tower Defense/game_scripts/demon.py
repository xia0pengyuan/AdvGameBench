import pygame
import constants as c
import sys
import time

class Demon(pygame.sprite.Sprite):
    def __init__(self, pos, name="NormalDemon", health=10, speed=2):
        super().__init__()
        self.image = pygame.Surface((c.CELL_WIDTH, c.CELL_HEIGHT))
        self.image.fill(c.RED)
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        self.under_dark_magic = False
        self.damage = 1
        self.dot_active = False
        self.dot_end_time = 0
        self.dot_next_tick = 0
        self.slow_active = False
        self.max_health =  health

        self.name = name
        self.health = health
        self.speed = speed /c.TIME_SCALE
        self.base_speed = speed / c.TIME_SCALE
        self.dot_tick_interval = 1000 * c.TIME_SCALE
        self.attack_interval = 1000 * c.TIME_SCALE
        self.last_attack_time = pygame.time.get_ticks()
        self.is_attacking = False  
        self.shake_frames = 0  

    def draw_text(self):
        font = pygame.font.Font(None, c.FONT_SIZE)
        text_surface = font.render(self.name, True, c.BLACK)
        text_rect = text_surface.get_rect(center=(self.image.get_width() // 2, self.image.get_height() // 2))
        self.image.blit(text_surface, text_rect)

    def attack_shake(self):
        if self.shake_frames > 0:
            self.rect.x += (-5 if self.shake_frames % 2 == 0 else 5)  
            self.shake_frames -= 1

    def attack(self, human_group):
        now = pygame.time.get_ticks()

        human_collisions = pygame.sprite.spritecollide(self, human_group, False)
        if human_collisions:
            if not self.is_attacking:
                self.is_attacking = True 

            if now - self.last_attack_time >= self.attack_interval:
                for human in human_collisions:
                    human.take_damage(self.damage)  
                    if human.health <= 0:
                        self.is_attacking = False  # 
                self.last_attack_time = now  
                self.shake_frames = 6  
            return True  #
        return False  
    
    def take_damage(self, damage, damage_type=None):
        if self.name =='FireDemon' and damage_type == c.fire:
            return
        elif self.name =='FrostDemon' and damage_type == c.fire:
            damage = 5
        
        if self.under_dark_magic and damage_type != "light" and damage < 20:
            return
        self.health -= damage
        if self.health <= 0:
            self.kill()

        
    def slow(self, duration):

        if self.name == "FrostDemon":
            return

        if self.name == "FireDemon":
            damage = 2
            self.health -= damage
            self.speed = self.base_speed * 0.5 
            if self.health <= 0:
                self.kill()
                return
        self.health -= 1
        current_time = pygame.time.get_ticks()
        self.slow_active = True
        self.speed = self.base_speed * 0.5  
        self.slow_end_time = current_time + duration
        if self.health <= 0:
                self.kill()
                return
                

    def update_effects(self):
        current_time = pygame.time.get_ticks()

        if self.slow_active and current_time >= self.slow_end_time:
            self.slow_active = False
            self.speed = self.base_speed

    def move(self):
        self.rect.x -= self.speed  

    def update(self, humans_group, demon_group=None):
        self.update_effects()
        if self.shake_frames > 0:
            self.attack_shake()
            return  

        if self.attack(humans_group): 
            return 
        
        self.is_attacking = False
        self.move()
        self.victory()

    def victory(self):
        if self.rect.right < 0:
            self.kill()
            pygame.quit()
            sys.exit()


class NormalDemon(Demon):
    def __init__(self, pos):
        super().__init__(pos)
        self.name ="NormalDemon"
        self.draw_text()

class GreatDemon(Demon):
    def __init__(self, pos):
        super().__init__(pos)
        self.name = "GreatDemon"
        self.health = 20 
        self.draw_text()


class DemonKing(Demon):
    def __init__(self, pos):
        super().__init__(pos)
        self.name = "DemonKing"
        self.health = 40
        self.damage = 5
        self.draw_text()

class SpeedyDemon(Demon):
    def __init__(self, pos):
        super().__init__(pos)
        self.name = "SpeedyDemon"
        self.speed = 4  /c.TIME_SCALE
        self.draw_text()


class ShieldDemon(Demon):
    def __init__(self, pos):
        super().__init__(pos)
        self.name = "ShieldDemon" 
        self.health = 10 
        self.shield = True
        self.draw_text()

    def take_damage(self, damage, damage_type=None):
        if self.shield and damage_type == c.normal:
            damage = float(damage * 0.3)
        super().take_damage(damage, damage_type)


class MachineDemon(Demon):
    def __init__(self, pos):
        super().__init__(pos)
        self.name = "MachineDemon" 
        self.machine_body = True  
        self.health = 20
        self.draw_text()

    def take_damage(self, damage, damage_type=None):
        if self.machine_body:
            self.damage = 3
            self.speed = 3 / c.TIME_SCALE
        super().take_damage(damage, damage_type)


class BouncingDemon(Demon):
    def __init__(self, pos):
        super().__init__(pos)
        self.name = "BouncingDemon" 
        self.has_jumped = False 
        self.draw_text()

    def update(self, humans_group):
        human_collisions = pygame.sprite.spritecollide(self, humans_group, False)
        for human in human_collisions:
            if human.name == "EnhancedShieldSoldier":
                super().update(humans_group) 
                return                

        if human_collisions and not self.has_jumped:
            self.rect.x -= c.CELL_WIDTH * 2  # 向后跳
            self.has_jumped = True  
            return
        else:
            super().update(humans_group)

    

class ShieldBreakerDemon(Demon):
    def __init__(self, pos):
        super().__init__(pos)
        self.name = "ShieldBreakerDemon"
        self.draw_text()

    def attack(self, human_group):
        now = pygame.time.get_ticks()

        human_collisions = pygame.sprite.spritecollide(self, human_group, False)
        if human_collisions:
            if not self.is_attacking:
                self.is_attacking = True

            if now - self.last_attack_time >= self.attack_interval:
                for human in human_collisions:
                    damage = 1 
                    if human.name =='ShieldSoldier' or  human.name == 'EnhancedShieldSoldier':
                        damage *= 5 

                    human.take_damage(damage)

                    if human.health <= 0:
                        self.is_attacking = False  
                self.last_attack_time = now  
                self.shake_frames = 6  
            return True  
        return False      

class FireDemon(Demon):
    def __init__(self, pos):
        super().__init__(pos)
        self.name = "FireDemon"
        self.draw_text()

    def take_damage(self, damage, damage_type=None):
        if damage_type == c.fire:
            return
        super().take_damage(damage, damage_type)


class FrostDemon(Demon):
    def __init__(self, pos):
        super().__init__(pos)
        self.name = "FrostDemon"
        self.draw_text()

    def take_damage(self, damage, damage_type=None):
        if damage_type == c.ice:
            return
        super().take_damage(damage, damage_type)


class FlyingDemon(Demon):
    def __init__(self, pos):
        super().__init__(pos)
        self.name = "FlyingDemon"
        self.health = 5
        self.draw_text()

    def update(self, humans_group, demon_group=None):
        self.update_effects()
        if self.shake_frames > 0:
            self.attack_shake()
            return
        self.is_attacking = False
        self.move()
        self.victory()

    def take_damage(self, damage, damage_type=None):
        if damage_type == c.fly:
            super().take_damage(damage, damage_type)


class ShadowDemon(Demon):
    def __init__(self, pos):
        super().__init__(pos)
        self.name = "ShadowDemon"
        self.draw_text()

    def cast_dark_magic(self, friendly_demon_group):

        for demon in friendly_demon_group:
            if demon.rect.x < self.rect.x and demon.rect.y == self.rect.y:
                demon.under_dark_magic = True


class SummoningDemon(Demon):      
    def __init__(self, pos):
        super().__init__(pos)
        self.name = "SummoningDemon"
        self.draw_text()
        self.speed = 1 / c.TIME_SCALE
        self.summoning_interval = 5000 * c.TIME_SCALE  
        self.last_summon_time = pygame.time.get_ticks()

    def summon(self, demons_group):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_summon_time >= self.summoning_interval:
            # 确保中心坐标在网格范围内
            center_x = max(0, min(self.rect.centerx, c.GRID_COLS * c.CELL_WIDTH - 1))
            center_y = max(0, min(self.rect.centery, c.GRID_ROWS * c.CELL_HEIGHT - 1))

            col = center_x // c.CELL_WIDTH
            row = center_y // c.CELL_HEIGHT

            summon_col = max(0, col - 1)
            summon_col = min(summon_col, c.GRID_COLS - 1)

            summon_x = summon_col * c.CELL_WIDTH + c.CELL_WIDTH // 2
            summon_y = row * c.CELL_HEIGHT + c.CELL_HEIGHT // 2 - c.CELL_HEIGHT

            new_demon = NormalDemon((summon_x, summon_y))
            demons_group.add(new_demon)
            self.last_summon_time = current_time
        
        

       