import pygame
import json
import minions as m
import constants as c
import board as b
import sys
import prompt as p
import re

class Game:
    def __init__(self, invaders_data, defenders_data):
        self.screen = pygame.display.set_mode((c.SCREEN_WIDTH, c.SCREEN_HEIGHT))
        pygame.display.set_caption("Battle Game")
        self.clock = pygame.time.Clock()
        self.running = True
        self.font = pygame.font.SysFont(None, 20)
        
        self.invaders = None
        self.defenders = None
        self.target_priority_for_invaders = None
        self.target_priority_for_defenders  = None
        
        self.round_number = 1
        self.attacker_team = None
        self.defender_team = None
        
        self.board = None
        
        self.animation_in_progress = False
        self.animation_step = 0
        self.animation_max_steps = 5 
        self.current_attacker = None
        self.current_target = None
        
        self.load_from_json(invaders_data, defenders_data)
        self.initialize_battle()
    
    def load_from_json(self, invaders_data, defenders_data):


        self.invaders = Team("Invaders")   
        self.defenders = Team("Defenders")    

        invaders_members = invaders_data.get("invaders", [])
        self.target_priority_for_invaders = invaders_data.get("target_priority_for_invaders", [])

        defenders_members = defenders_data.get("defenders", [])
        self.target_priority_for_defenders = defenders_data.get("target_priority_for_defenders", [])

        
        for invader in invaders_members:
            name = invader.get('name')
            tier = invader.get('tier') or 'Bronze'

            if name == c.FIRE_LIZARD:
                minion = m.FireLizard(tier)
            elif name == c.WATER_ELEMENTAL:
                minion = m.WaterElemental(tier)
            elif name == c.POISON_FROG:
                minion = m.PoisonFrog(tier)
            elif name == c.MOLTEN_HOUND:
                minion = m.MoltenHound(tier)
            elif name == c.BATTLE_FRENZY:
                minion = m.BattleFrenzy(tier)
            elif name == c.TIDE_GUARDIAN:
                minion = m.TideGuardian(tier)
            elif name == c.LAVA_GOLEM:
                minion = m.LavaGolem(tier)
            elif name == c.BANDIT_LEADER:
                minion = m.BanditLeader(tier)
            elif name == c.PHOENIX:
                minion = m.Phoenix(tier)
            elif name == c.SHADOW_OVERLORD:
                minion = m.ShadowOverlord(tier)
            elif name == c.TIDE_LORD:
                minion = m.TideLord(tier)
            else:
                continue
            self.invaders.add_minion(minion)
        
        for defender in defenders_members:
            name = defender.get('name')
            tier = defender.get('tier') or 'Bronze'

            if name == c.SAPLING:
                minion = m.Sapling(tier)  
            elif name == c.ROCK_BEETLE:
                minion = m.RockBeetle(tier)
            elif name == c.FOREST_SEER:
                minion = m.ForestSeer(tier)
            elif name == c.STONE_WARRIOR:
                minion = m.StoneWarrior(tier)
            elif name == c.ELITE_SOLDIER:
                minion = m.EliteSoldier(tier)
            elif name == c.VINE_PROTECTOR:
                minion = m.VineProtector(tier)
            elif name == c.BLACK_ROCK:
                minion = m.BlackRock(tier)
            elif name == c.PALADIN:
                minion = m.Paladin(tier)
            elif name == c.MOUNTAIN_GIANT:
                minion = m.MountainGiant(tier)
            elif name == c.KING:
                minion = m.King(tier)
            elif name == c.ANCIENT_TREANT:
                minion = m.AncientTreant(tier)
            else:
                continue
            self.defenders.add_minion(minion)
    
    def initialize_battle(self):
        self.board = b.Board(self.invaders, self.defenders)
    
    def run(self):
        while self.running and not self.invaders.is_defeated() and not self.defenders.is_defeated():
            self.clock.tick(60)
            self.handle_events()
            
            if self.animation_in_progress:
                self.update_animation()
            else:
                self.update()
                    
            self.draw()
            
        if self.running:
            self.draw_winner()
            pygame.time.delay(500)
            
        pygame.quit()
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
    
    def update_animation(self):
        self.animation_step += 1
        
        if self.animation_step >= self.animation_max_steps:
            if self.current_attacker in self.invaders.minions:
                enemy_team = self.defenders.minions
                friendly_minions = self.invaders.minions
            else:
                enemy_team = self.invaders.minions
                friendly_minions = self.defenders.minions


            # 执行攻击
            self.current_attacker.attack_target(self.current_target, enemy_team, friendly_minions)
            self.invaders.remove_dead()
            self.defenders.remove_dead()

            
            self.handle_death_effects()

            self.animation_in_progress = False
            self.animation_step = 0
            self.current_attacker = None
            self.current_target = None
            
            pygame.time.delay(c.ATTACK_DELAY)
    
    def handle_death_effects(self):
        
        for team in [self.invaders, self.defenders]:
            dead_minions = [m for m in team.dead_minions if not m.death_processed]
            for dead_minion in dead_minions:
                if dead_minion.name == c.SHADOW_OVERLORD:
                    self.process_shadow_overlord_death(dead_minion, team)
                if dead_minion.name == c.STONE_WARRIOR:
                    empty_slots = 7 - len(team.minions)
                    if empty_slots <= 0:
                        return
                    minion = m.RockBeetle(dead_minion.tier)
                    team.add_minion(minion)
                dead_minion.death_processed = True
            team.dead_minions.clear()

    def process_shadow_overlord_death(self, shadow_overlord, team):
        """处理 Shadow Overlord 死亡后的效果"""
        empty_slots = 7 - len(team.minions)
        if empty_slots <= 0:
            return

        for _ in range(empty_slots):
            skeleton = m.SkeletonMinion(shadow_overlord.tier)
            team.add_minion(skeleton)
        

    def update(self):
        for minion in self.invaders.minions:
            if hasattr(minion, 'on_game_start'):
                minion.on_game_start(self.invaders.minions)
        for minion in self.defenders.minions:
            if hasattr(minion, 'on_game_start'):
                minion.on_game_start(self.defenders.minions)
        

        inv_start_alive = self.invaders.get_alive()
        def_start_alive = self.defenders.get_alive()
        if len(inv_start_alive) >= len(def_start_alive):
            first_attacker_team = 'invaders'
        else:
            first_attacker_team = 'defenders'
        
        while self.invaders.get_alive() and self.defenders.get_alive():
            
            inv_alive = self.invaders.get_alive()
            def_alive = self.defenders.get_alive()
            
            if first_attacker_team == 'invaders':
                invader_list_snapshot = inv_alive[:]
                
                for invader in invader_list_snapshot:
                    inv_alive = self.invaders.get_alive()
                    def_alive = self.defenders.get_alive()
                    if not inv_alive or not def_alive:
                        break
                    
                    if invader not in inv_alive:
                        continue
                    
                    attacker = invader
                    target = def_alive[0] 
                    attacker_team_name = self.invaders.name
                    enemy_team_name = self.defenders.name
                    
                    action_text = f"{attacker_team_name} 的 {attacker.name} 攻击 {enemy_team_name} 的 {target.name}"
                    
                    self.screen.fill(c.WHITE)
                    self.board.draw(self.screen, self.font)
                    action_surface = self.font.render(action_text, True, (200, 0, 0))
                    self.screen.blit(action_surface, (50, c.SCREEN_HEIGHT - 40))
                    pygame.display.update()

                    self.animation_in_progress = True
                    self.animation_step = 0
                    self.current_attacker = attacker
                    self.current_target = target

                    while self.animation_in_progress and self.running:
                        self.clock.tick(60)
                        self.handle_events()
                        self.update_animation()
                        self.draw()
                    
                    if not self.defenders.get_alive():
                        break
                    
                    inv_alive = self.invaders.get_alive()
                    def_alive = self.defenders.get_alive()
                    if not inv_alive or not def_alive:
                        break
                    
                    defender_attacker = def_alive[0]
                    defender_target = inv_alive[0]
                    attacker_team_name = self.defenders.name
                    enemy_team_name = self.invaders.name
                    
                    action_text = f"{attacker_team_name} 的 {defender_attacker.name} 攻击 {enemy_team_name} 的 {defender_target.name}"
                    
                    self.screen.fill(c.WHITE)
                    self.board.draw(self.screen, self.font)
                    action_surface = self.font.render(action_text, True, (200, 0, 0))
                    self.screen.blit(action_surface, (50, c.SCREEN_HEIGHT - 40))
                    pygame.display.update()

                    self.animation_in_progress = True
                    self.animation_step = 0
                    self.current_attacker = defender_attacker
                    self.current_target = defender_target

                    while self.animation_in_progress and self.running:
                        self.clock.tick(60)
                        self.handle_events()
                        self.update_animation()
                        self.draw()
                    
                    if not self.invaders.get_alive():
                        break
            
            else:
                defender_list_snapshot = def_alive[:]
                for defender in defender_list_snapshot:
                    inv_alive = self.invaders.get_alive()
                    def_alive = self.defenders.get_alive()
                    if not inv_alive or not def_alive:
                        break
                    if defender not in def_alive:
                        continue
                    
                    attacker = defender
                    target = inv_alive[0]
                    attacker_team_name = self.defenders.name
                    enemy_team_name = self.invaders.name
                    
                    action_text = f"{attacker_team_name} 的 {attacker.name} 攻击 {enemy_team_name} 的 {target.name}"
                    
                    self.screen.fill(c.WHITE)
                    self.board.draw(self.screen, self.font)
                    action_surface = self.font.render(action_text, True, (200, 0, 0))
                    self.screen.blit(action_surface, (50, c.SCREEN_HEIGHT - 40))
                    pygame.display.update()

                    self.animation_in_progress = True
                    self.animation_step = 0
                    self.current_attacker = attacker
                    self.current_target = target

                    while self.animation_in_progress and self.running:
                        self.clock.tick(60)
                        self.handle_events()
                        self.update_animation()
                        self.draw()
                    
                    if not self.invaders.get_alive():
                        break
                    
                    inv_alive = self.invaders.get_alive()
                    def_alive = self.defenders.get_alive()
                    if not inv_alive or not def_alive:
                        break
                    
                    inv_attacker = inv_alive[0]
                    inv_target = def_alive[0]
                    attacker_team_name = self.invaders.name
                    enemy_team_name = self.defenders.name
                    
                    action_text = f"{attacker_team_name} 的 {inv_attacker.name} 攻击 {enemy_team_name} 的 {inv_target.name}"
                    
                    self.screen.fill(c.WHITE)
                    self.board.draw(self.screen, self.font)
                    action_surface = self.font.render(action_text, True, (200, 0, 0))
                    self.screen.blit(action_surface, (50, c.SCREEN_HEIGHT - 40))
                    pygame.display.update()

                    self.animation_in_progress = True
                    self.animation_step = 0
                    self.current_attacker = inv_attacker
                    self.current_target = inv_target

                    while self.animation_in_progress and self.running:
                        self.clock.tick(60)
                        self.handle_events()
                        self.update_animation()
                        self.draw()
                    
                    if not self.defenders.get_alive():
                        break

            self.round_number += 1
            
           
    
    def draw(self):
        self.screen.fill(c.WHITE)
        round_text = self.font.render(f"=== 第 {self.round_number} 回合 ===", True, c.BLACK)
        self.screen.blit(round_text, (c.SCREEN_WIDTH // 2 - round_text.get_width() // 2, 10))
        
        self.board.draw(self.screen, self.font, 
                         current_attacker=self.current_attacker,
                         current_target=self.current_target,
                         animation_in_progress=self.animation_in_progress,
                         animation_step=self.animation_step,
                         animation_max_steps=self.animation_max_steps,
                         attacker_team=self.attacker_team,
                         defender_team=self.defender_team)
        
        if self.animation_in_progress and self.current_attacker and self.current_target:
            action_text = f"{self.invaders.name} 的 {self.current_attacker.name} 攻击 {self.defenders.name} 的 {self.current_target.name}"
            action_surface = self.font.render(action_text, True, c.RED)
            self.screen.blit(action_surface, (50, c.SCREEN_HEIGHT - 40))
            
        pygame.display.update()
    
    def parse_minion_costs(self, prompt_str):

        cost_dict = {}
        for line in prompt_str.splitlines():
            line = line.strip()
            if not line:
                continue
            # 角色名称为冒号前的部分
            name = line.split(":", 1)[0].strip()
            # 查找 "Cost:" 后的数字
            match = re.search(r"Cost:\s*(\d+)", line)
            if match:
                cost = int(match.group(1))
                cost_dict[name] = cost
        return cost_dict

    def draw_winner(self):
        invader_costs = self.parse_minion_costs(p.invader_information)
        defender_costs = self.parse_minion_costs(p.defender_information)
        
        if self.defenders.is_defeated():
            winner_team = self.invaders
            winner_costs = invader_costs
        else:
            winner_team = self.defenders
            winner_costs = defender_costs

        remaining_count = len(winner_team.minions)
        
        total_cost = 0
        for minion in winner_team.minions:
            cost = winner_costs.get(minion.name, 0)
            if getattr(minion, "tier", "").lower() == "gold":
                cost *= 2
            total_cost += cost

        winner_text = (
        f"{winner_team.name} win! "
        f"Invader remain: {len(self.invaders.minions)}, "
        f"Defender remain: {len(self.defenders.minions)}, "
    )
        
        self.screen.fill(c.WHITE)
        self.board.draw(self.screen, self.font)
        win_surface = self.font.render(winner_text, True, c.GREEN)
        self.screen.blit(win_surface, (c.SCREEN_WIDTH // 2 - win_surface.get_width() // 2, c.SCREEN_HEIGHT - 60))
        pygame.display.update()
        print(winner_text)
    
    def choose_target(self, enemy_minions):
        taunt_targets = [minion for minion in enemy_minions if "Taunt" in getattr(minion, "abilities", [])]
        if taunt_targets:
            return taunt_targets[0]
        if enemy_minions:
            return enemy_minions[0]
        return None


class Team:
    def __init__(self, name):
        self.name = name
        self.minions = []  
        self.dead_minions = []  

    def add_minion(self, minion):
        if len(self.minions) < 7:
            self.minions.append(minion)
            return True
        else:
            return False

    def remove_dead(self):
        for minion in list(self.minions):
            if minion.health <= 0:
                self.dead_minions.append(minion)
        
        self.minions = [minion for minion in self.minions if minion.health > 0]

    def is_defeated(self):
        return len(self.minions) == 0

    def get_alive(self):
        return self.minions

if __name__ == "__main__":
    
    try:
        pygame.init()
        pygame.font.init()  
        if len(sys.argv) < 3:
            print("Usage: python game.py '<human_data_json>' '<demon_data_json>'")
            sys.exit(1)
        
        defender_data = json.loads(sys.argv[1])
        invader_data = json.loads(sys.argv[2])
        
        game = Game(invader_data, defender_data)
        game.run()
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
        """
    pygame.init()
    pygame.font.init()  
    with open("invaders.json", "r", encoding="utf-8") as f:
        invader_data = json.load(f)
    with open("defenders.json", "r", encoding="utf-8") as f: 
        defender_data = json.load(f)

    game = Game(invader_data, defender_data)
    game.run()
    """