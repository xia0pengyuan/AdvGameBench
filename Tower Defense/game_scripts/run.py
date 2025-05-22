import pygame
import sys
import json
import constants as c
import human as h
import demon as d
import re
import prompt as p

pygame.init()

def getPixelPos(grid_x, grid_y):
    x = grid_x * c.CELL_WIDTH + c.CELL_WIDTH // 2 
    y = grid_y * c.CELL_HEIGHT + c.CELL_HEIGHT // 2 
    return x, y

def parse_character_costs(prompt_str):

    cost_dict = {}
    for line in prompt_str.splitlines():
        line = line.strip()
        # 过滤掉不符合格式的行
        if not line or ':' not in line:
            continue
        # 使用正则表达式查找 cost 后面的数字
        match = re.search(r"cost:\s*(\d+)", line)
        if match:
            cost = int(match.group(1))
            # 角色名为冒号前的部分
            name = line.split(":", 1)[0].strip()
            cost_dict[name] = cost
    return cost_dict



def get_character_cost(character_name, faction='human'):
    human_costs = parse_character_costs(p.human)
    demon_costs = parse_character_costs(p.demon)
    if faction == 'human':
        return human_costs.get(character_name, 0)
    elif faction == 'demon':
        return demon_costs.get(character_name, 0)
    else:
        raise ValueError("faction 必须为 'human' 或 'demon'")

class Game:
    def __init__(self,human_data, demon_data):
        self.screen = pygame.display.set_mode((c.SCREEN_WIDTH, c.SCREEN_HEIGHT))
        pygame.display.set_caption("game1")
        self.clock = pygame.time.Clock()
        self.running = True
        
        self.human_group = pygame.sprite.Group()
        self.demon_group = pygame.sprite.Group()
        self.bullet_group = pygame.sprite.Group()
        self.explosion_log = []
        self.grid = [[(col * c.CELL_WIDTH + 40, row * c.CELL_HEIGHT + 40) 
                      for col in range(c.GRID_COLS)] for row in range(c.GRID_ROWS)]
        
        self.human_spawn_events = []
        self.demon_spawn_events = []
        self.game_result = None
        """
        with open('human.json', "r", encoding="utf-8") as file:
            human_data = json.load(file)
        with open('demon.json', "r", encoding="utf-8") as file:
            demon_data = json.load(file)
       """


        for human in human_data.get("humans", []):
            self.human_spawn_events.append(human)
        self.human_spawn_events.sort(key=lambda p: p['spawn_time'])

        for demon in demon_data.get("demons", []):
            self.demon_spawn_events.append(demon)
        self.demon_spawn_events.sort(key=lambda z: z['spawn_time'])

        for ev in self.human_spawn_events:
            ev['spawn_time'] = int(ev['spawn_time'] * c.TIME_SCALE)
        for ev in self.demon_spawn_events:
            ev['spawn_time'] = int(ev['spawn_time'] * c.TIME_SCALE)

    def run(self):
        while self.running:
            self.clock.tick(c.FPS)
            self.handle_events()
            self.update()
            self.draw()

        # 游戏结束后计算剩余角色数量和总 cost
        if self.game_result:
            if "Human win" in self.game_result:
                winner_group = self.human_group
                faction = "human"
            elif "Demon win" in self.game_result:
                winner_group = self.demon_group
                faction = "demon"
            else:
                winner_group = None

            if winner_group is not None:
                remaining_count = len(winner_group)
                # 使用 get_character_cost 来获取每个角色的 cost
                total_cost = sum(get_character_cost(unit.name, faction) for unit in winner_group)
                self.game_result += f" | remain characters: {remaining_count}, cost: {total_cost}"

        print(self.game_result)
        pygame.quit()
        sys.exit()
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def update(self):
        current_time = pygame.time.get_ticks()  

        while self.human_spawn_events and self.human_spawn_events[0]['spawn_time'] <= current_time:
            event = self.human_spawn_events.pop(0)
            name = event['name']
            map_x = event['x']
            map_y = event['y']
            map_x, map_y = getPixelPos(map_x, map_y)

            if name == 'HandgunSoldier':
                new_soldier = h.HandgunSoldier((map_x, map_y))
            elif name == 'RifleSoldier':
                new_soldier = h.RifleSoldier((map_x, map_y))
            elif name == 'MachineGunSoldier':
                new_soldier = h.MachineGunSoldier((map_x, map_y))
            elif name == 'ShieldSoldier':
                new_soldier = h.ShieldSoldier((map_x, map_y))
            elif name == 'EnhancedShieldSoldier':
                new_soldier = h.EnhancedShieldSoldier((map_x, map_y))
            elif name == 'FlamethrowerSoldier':
                new_soldier = h.FlamethrowerSoldier((map_x, map_y))
            elif name == 'IceSoldier':
                new_soldier = h.IceSoldier((map_x, map_y))
            elif name == 'AntiAirSoldier':
                new_soldier = h.AntiAirSoldier((map_x, map_y))
            elif name == 'Bomb':
                new_soldier = h.Bomb((map_x, map_y))
            elif name == 'LinearExplosion':
                new_soldier = h.LinearExplosion((map_x, map_y))
            elif name == 'MagneticSoldier':
                new_soldier = h.MagneticSoldier((map_x, map_y))
            else:
                continue
            self.human_group.add(new_soldier)

        while self.demon_spawn_events and self.demon_spawn_events[0]['spawn_time'] <= current_time:
            event = self.demon_spawn_events.pop(0)
            name = event['name']
            map_x = 11
            map_y = event['y']
            map_x, map_y = getPixelPos(map_x, map_y)

            if name == 'NormalDemon':
                new_demon = d.NormalDemon((map_x, map_y))
            elif name == 'GreatDemon':
                new_demon = d.GreatDemon((map_x, map_y))
            elif name == 'DemonKing':
                new_demon = d.DemonKing((map_x, map_y))
            elif name == 'ShieldDemon':
                new_demon = d.ShieldDemon((map_x, map_y))
            elif name == 'MachineDemon':
                new_demon = d.MachineDemon((map_x, map_y))
            elif name == 'BouncingDemon':
                new_demon = d.BouncingDemon((map_x, map_y))
            elif name == 'ShieldBreakerDemon':
                new_demon = d.ShieldBreakerDemon((map_x, map_y))
            elif name == 'FireDemon':
                new_demon = d.FireDemon((map_x, map_y))
            elif name == 'FrostDemon':
                new_demon = d.FrostDemon((map_x, map_y))
            elif name == 'FlyingDemon':
                new_demon = d.FlyingDemon((map_x, map_y))
            elif name == 'SpeedyDemon':
                new_demon = d.SpeedyDemon((map_x, map_y))
            elif name == 'SummoningDemon':
                new_demon = d.SummoningDemon((map_x, map_y))
            elif name == 'HealingDemon':
                new_demon = d.HealingDemon((map_x, map_y))
            else:
                continue

            self.demon_group.add(new_demon)

        for demon in self.demon_group:
            if demon.name == "SummoningDemon":
                demon.summon(self.demon_group)


        for bullet in self.bullet_group:
            hit_demons = pygame.sprite.spritecollide(bullet, self.demon_group, False)
            if hit_demons:
                    bullet.hit_target(hit_demons[0])
                

        self.human_group.update(self.bullet_group, self.demon_group)
        self.demon_group.update(self.human_group)
        self.bullet_group.update()

        for demon in self.demon_group:
            if demon.rect.left <= 40:
                y_pos = demon.rect.centery
                lost_row = (y_pos - 40) // c.CELL_HEIGHT
                self.game_result = f"Demon win! Lost grid row: {lost_row}"
                self.running = False
                break

        if not self.demon_group and not self.demon_spawn_events:
            self.game_result = "Human win!"
            self.running = False

    def draw(self):
        self.screen.fill(c.BLACK)
        
        for row in range(c.GRID_ROWS):
            for col in range(c.GRID_COLS):
                rect = pygame.Rect(self.grid[row][col], (c.CELL_WIDTH, c.CELL_HEIGHT))
                pygame.draw.rect(self.screen, c.WHITE, rect, 1)
        
        self.human_group.draw(self.screen)
        self.demon_group.draw(self.screen)
        self.bullet_group.draw(self.screen)
        
        pygame.display.flip()

if __name__ == "__main__":

    """
    with open('human.json', "r", encoding="utf-8") as file:
        human_data = json.load(file)



    with open('demon.json', "r", encoding="utf-8") as file:
        demon_data = json.load(file)

    pygame.init()
    game = Game(human_data, demon_data)
    game.run()

    """
    try:
        pygame.init()
        pygame.font.init()  
        if len(sys.argv) < 3:
            print("Usage: python game.py '<human_data_json>' '<demon_data_json>'")
            sys.exit(1)
        
        human_data = json.loads(sys.argv[1])
        demon_data = json.loads(sys.argv[2])
        
        game = Game(human_data, demon_data)
        game.run()
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
        