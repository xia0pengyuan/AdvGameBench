import pygame
import constants as c

class human(pygame.sprite.Sprite):

    def __init__(self, pos, health=3, shoot_interval=1000, name="human"):
        super().__init__()
        self.image = pygame.Surface((c.CELL_WIDTH, c.CELL_HEIGHT ))
        self.image.fill(c.GREEN)
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        

        self.health = health
        self.shoot_interval = shoot_interval * c.TIME_SCALE if shoot_interval else None
        self.last_shot_time = pygame.time.get_ticks()

        self.name = name
        self.draw_text()

    def draw_text(self):
        self.image.fill(c.GREEN)
        font = pygame.font.Font(None, c.FONT_SIZE) 
        text_surface = font.render(self.name, True, c.BLACK)
        text_rect = text_surface.get_rect(center=(self.image.get_width() // 2, self.image.get_height() // 2))
        self.image.blit(text_surface, text_rect)

    def update(self, bullets_group, demon_group):
        pass

    def take_damage(self,damage):
        self.health -= damage
        if self.health <= 0:
            self.kill()  # 生命值归零时，植物被摧毁


class HandgunSoldier(human):
    def __init__(self, pos):
        super().__init__(pos,  name="HandgunSoldier")
        self.draw_text()

    def update(self, bullets_group, demon_group):
        now = pygame.time.get_ticks()
        if now - self.last_shot_time >= self.shoot_interval:
            bullet = Bullet((self.rect.right, self.rect.centery))
            bullets_group.add(bullet)
            self.last_shot_time = now


class RifleSoldier(human):
    def __init__(self, pos):
        super().__init__(pos,  shoot_interval=500, name="RifleSoldier")
        self.draw_text()

    def update(self, bullets_group, demon_group):
        now = pygame.time.get_ticks()
        if now - self.last_shot_time >= self.shoot_interval:
            bullet = Bullet((self.rect.right, self.rect.centery))
            bullets_group.add(bullet)
            self.last_shot_time = now

class MachineGunSoldier(human):
    def __init__(self, pos):
        super().__init__(pos,  shoot_interval=250, name="MachineGunSoldier")
        self.image.fill(c.GREEN)
        self.draw_text()

    def update(self, bullets_group, demon_group):
        now = pygame.time.get_ticks()
        if now - self.last_shot_time >= self.shoot_interval:
            bullet = Bullet((self.rect.right, self.rect.centery))
            bullets_group.add(bullet)
            self.last_shot_time = now

class ShieldSoldier(human):
    def __init__(self, pos):
        super().__init__(pos, health=15, shoot_interval=None, name="ShieldSoldier")
        self.draw_text()

    def update(self, bullets_group, demon_group):
        pass

class EnhancedShieldSoldier(human):
    def __init__(self, pos):
        super().__init__(pos, health=30, shoot_interval=None, name="EnhancedShieldSoldier")
        self.draw_text()


class FlamethrowerSoldier(human):
    def __init__(self, pos):
        super().__init__(pos, health=2, name="FlamethrowerSoldier")
        self.draw_text()

    def update(self, bullets_group, demon_group):
        now = pygame.time.get_ticks()
        if now - self.last_shot_time >= self.shoot_interval:
            bullet = FireBullet((self.rect.right, self.rect.centery))
            bullets_group.add(bullet)
            self.last_shot_time = now

class IceSoldier(human):
    def __init__(self, pos):
        super().__init__(pos, health=2, name="IceSoldier")
        self.draw_text()

    def update(self, bullets_group, demon_group):
        now = pygame.time.get_ticks()
        if now - self.last_shot_time >= self.shoot_interval:
            bullet = IceBullet((self.rect.right, self.rect.centery))
            bullets_group.add(bullet)
            self.last_shot_time = now

class AntiAirSoldier(human):
    def __init__(self, pos):
        super().__init__(pos, health=2, name="AntiAirSoldier")
        self.draw_text()
    
    def update(self, bullets_group, demon_group):
        now = pygame.time.get_ticks()
        if now - self.last_shot_time >= self.shoot_interval:
            bullet = AntiAirBullet((self.rect.right, self.rect.centery))
            bullets_group.add(bullet)
            self.last_shot_time = now


class Bomb(human):
    bomb_counter = 0  

    def __init__(self, pos):
        super().__init__(pos)
        self.name = 'Bomb'
        self.draw_text()
        self.health = 50
        self.damage = 30
        self.explosion_time = pygame.time.get_ticks() + 500 * c.TIME_SCALE 
        self.exploded = False 
        Bomb.bomb_counter += 1  
        self.bomb_id = Bomb.bomb_counter 
        self.killed_demons = 0  

    def update(self, bullets_group, demon_group):
        self.explode(demon_group)

    def explode(self, demon_group):
        if not self.exploded and pygame.time.get_ticks() >= self.explosion_time:
            self.exploded = True
        grid_x = self.rect.x // c.CELL_WIDTH
        grid_y = self.rect.y // c.CELL_HEIGHT

        explosion_positions = [
            (grid_x, grid_y),  
            (grid_x - 1, grid_y),  
            (grid_x + 1, grid_y),  
            (grid_x, grid_y - 1),  
            (grid_x, grid_y + 1)   
        ]

        explosion_areas = [
            pygame.Rect(x * c.CELL_WIDTH, y * c.CELL_HEIGHT, c.CELL_WIDTH, c.CELL_HEIGHT)
            for x, y in explosion_positions
        ]

        for demon in demon_group:
            if any(explosion_rect.colliderect(demon.rect) for explosion_rect in explosion_areas):
                demon.take_damage(self.damage)
                self.killed_demons += 1  

        self.kill()


class LinearExplosion(human):
    linear_explosion_counter = 0  

    def __init__(self, pos):
        super().__init__(pos)
        self.name = "LinearExplosion"
        self.draw_text()
        self.health = 50
        self.damage = 30
        self.explosion_time = pygame.time.get_ticks() + 500 * c.TIME_SCALE
        self.exploded = False  
        LinearExplosion.linear_explosion_counter += 1
        self.explosion_id = LinearExplosion.linear_explosion_counter 

    def update(self, bullets_group, demon_group):
        if not self.exploded and pygame.time.get_ticks() >= self.explosion_time:
            self.explode(demon_group)

    def explode(self, demon_group):
        self.exploded = True  
        grid_x = self.rect.x // c.CELL_WIDTH
        grid_y = self.rect.y // c.CELL_HEIGHT

        explosion_areas = [
            pygame.Rect(x, grid_y * c.CELL_HEIGHT, c.CELL_WIDTH, c.CELL_HEIGHT)
            for x in range(0, c.SCREEN_WIDTH, c.CELL_WIDTH)
        ]

        for demon in demon_group:
            if any(explosion_rect.colliderect(demon.rect) for explosion_rect in explosion_areas):
                demon.take_damage(self.damage)

        self.kill()  


class MagneticSoldier(human):
    def __init__(self, pos):
        super().__init__(pos, health=2, shoot_interval=2000, name="MagneticSoldier")
        self.draw_text()
        self.magnetic_range = c.CELL_WIDTH * (c.GRID_COLS - 1)

    def magnetic_pulse(self, demon_group):
        for demon in demon_group:
            if (demon.name == "ShieldDemon" and 
            (self.rect.y // c.CELL_HEIGHT) == (demon.rect.y // c.CELL_HEIGHT) and
            self.rect.centerx - self.magnetic_range <= demon.rect.centerx <= self.rect.centerx + self.magnetic_range):
                demon.shield = False  
            elif (demon.name == "MachineDemon"  and  (self.rect.y // c.CELL_HEIGHT) == (demon.rect.y // c.CELL_HEIGHT) and
            self.rect.centerx - self.magnetic_range <= demon.rect.centerx <= self.rect.centerx + self.magnetic_range):
                demon.machine_body = False


class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos, color=c.WHITE, damage_type=c.normal, speed=10):
        super().__init__()
        self.image = pygame.Surface((10, 5))
        self.image.fill(color)
        self.rect = self.image.get_rect(midleft=pos)
        self.damage = 1
        self.speed = speed/c.TIME_SCALE
        self.damage_type = damage_type
        self.name = 'Bullet'

    def update(self):
        self.rect.x += self.speed
        if self.rect.left > c.SCREEN_WIDTH:
            self.kill()

    def hit_target(self, demon):
        # 如果目标是 FlyingDemon 且该子弹不具备飞行属性，则忽略碰撞（即穿越过去）
        if demon.name == "FlyingDemon" and self.damage_type != c.fly:
            return
        demon.take_damage(self.damage, self.damage_type)
        self.kill()


class IceBullet(Bullet):
    def __init__(self, pos):
        super().__init__(pos)
        self.image = pygame.Surface((10, 5))
        self.image.fill(c.BLUE)
        self.damage_type = c.ice
        self.name = 'IceBullet'
        self.duration = 2000

    def hit_target(self, demon):
        if demon.name == "FlyingDemon" and self.damage_type != c.fly:
            return
        demon.slow(self.duration)
        self.kill()


class FireBullet(Bullet):
    def __init__(self, pos):
        super().__init__(pos)
        self.image = pygame.Surface((10, 5))
        self.image.fill(c.RED)
        self.damage_type = c.fire
        self.name = 'FireBullet'
        self.damage = 2

    def hit_target(self, demon):
        if demon.name == "FlyingDemon" and self.damage_type != c.fly:
            return
        demon.take_damage(self.damage, self.damage_type)
        self.kill()


class AntiAirBullet(Bullet):
    def __init__(self, pos):
        super().__init__(pos, color=c.YELLOW, damage_type=c.fly)
        self.name = "AntiAirBullet"

    def hit_target(self, demon):

        if demon.name == "FlyingDemon":
            demon.take_damage(self.damage, self.damage_type)
        else:
            return
        self.kill()