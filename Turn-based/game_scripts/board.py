import constants as c
import pygame


class Board: 
    def __init__(self, team_left, team_right):
        self.team_left = team_left
        self.team_right = team_right
        self.max_minions = 7  

        self.card_width = c.CARD_WIDTH
        self.card_height = c.CARD_HEIGHT
        self.card_gap = 20  

        self.middle_gap = 50
        
        self.left_start_x = (c.SCREEN_WIDTH - self.max_minions * (self.card_width + self.card_gap)) // 2
        
        # 计算两队的 Y 坐标位置
        self.top_team_y = c.SCREEN_HEIGHT // 2 - self.middle_gap // 2 - self.card_height
        self.bottom_team_y = c.SCREEN_HEIGHT // 2 + self.middle_gap // 2
        
        self.attack_move_distance_vertical = 15
        self.attack_move_distance_horizontal = 30  

    def draw(self, screen, font, current_attacker=None, current_target=None, 
             animation_in_progress=False, animation_step=0, animation_max_steps=0,
             attacker_team=None, defender_team=None):
        # 绘制中间分割线
        pygame.draw.line(screen, c.BLACK, 
                         (0, c.SCREEN_HEIGHT // 2), 
                         (c.SCREEN_WIDTH, c.SCREEN_HEIGHT // 2), 
                         2)

        is_cleave_attack = False
        if current_attacker is not None:
            if [att for att in [current_attacker] if "Cleave" in getattr(att, "abilities", [])]:
                is_cleave_attack = True

        # 针对左侧队伍：如果是 Cleave 攻击，则计算当前目标在队伍中的索引
        target_index_left = None
        if animation_in_progress and current_target and current_target in self.team_left.minions:
            target_index_left = self.team_left.minions.index(current_target)

        # 绘制左侧队伍
        for i, minion in enumerate(self.team_left.minions[:self.max_minions]):
            x = self.left_start_x + i * (self.card_width + self.card_gap)  
            y = self.top_team_y
            
            move_y = 0
            move_x = 0  
            if animation_in_progress and minion == current_attacker:
                if animation_step < animation_max_steps // 2:
                    move_ratio = animation_step / (animation_max_steps // 2)
                    move_y = self.attack_move_distance_vertical * move_ratio
                    move_x = self.attack_move_distance_horizontal * move_ratio  
                else:
                    move_ratio = 1 - ((animation_step - animation_max_steps // 2) / (animation_max_steps // 2))
                    move_y = self.attack_move_distance_vertical * move_ratio
                    move_x = self.attack_move_distance_horizontal * move_ratio
            
            rect = pygame.Rect(x + move_x, y + move_y, self.card_width, self.card_height)
            
            # 默认背景色
            bg_color = (230, 230, 230)
            # 根据是否为 Cleave 攻击采取不同的标红策略
            if animation_in_progress:
                if is_cleave_attack:
                    # Cleave 攻击：目标及左右相邻的随从标红
                    if target_index_left is not None:
                        if i in (target_index_left - 1, target_index_left, target_index_left + 1):
                            bg_color = c.RED
                else:
                    # 非 Cleave 攻击：只有被直接攻击的目标标红
                    if current_target is not None and minion == current_target:
                        bg_color = c.RED
            
            pygame.draw.rect(screen, bg_color, rect)
            pygame.draw.rect(screen, c.BLACK, rect, 2)
            
            name_surface = font.render(minion.name, True, c.BLACK)
            name_rect = name_surface.get_rect(center=(rect.centerx, rect.centery - 25))
            screen.blit(name_surface, name_rect)
            
            hp_surface = font.render(f"HP: {minion.health}", True, c.GREEN)
            hp_rect = hp_surface.get_rect(center=(rect.centerx, rect.centery))
            screen.blit(hp_surface, hp_rect)
            
            atk_surface = font.render(f"ATK: {minion.attack}", True, c.RED)
            atk_rect = atk_surface.get_rect(center=(rect.centerx, rect.centery + 25))
            screen.blit(atk_surface, atk_rect)
            
            # 新增：显示护盾信息，如果随从拥有圣盾
            if minion.has_divine_shield():
                shield_surface = font.render("Shield", True, c.BLUE)
                # 将“Shield”文字显示在卡牌的右上角
                shield_rect = shield_surface.get_rect()
                shield_rect.topright = (rect.right - 5, rect.top + 5)
                screen.blit(shield_surface, shield_rect)
        
        # 针对右侧队伍：如果是 Cleave 攻击，则计算当前目标在队伍中的索引
        target_index_right = None
        if animation_in_progress and current_target and current_target in self.team_right.minions:
            target_index_right = self.team_right.minions.index(current_target)
            
        for i, minion in enumerate(self.team_right.minions[:self.max_minions]):
            x = self.left_start_x + i * (self.card_width + self.card_gap) 
            y = self.bottom_team_y
            
            move_y = 0
            move_x = 0  
            if animation_in_progress and minion == current_attacker:
                if animation_step < animation_max_steps // 2:
                    move_ratio = animation_step / (animation_max_steps // 2)
                    move_y = -self.attack_move_distance_vertical * move_ratio
                    move_x = -self.attack_move_distance_horizontal * move_ratio  
                else:
                    move_ratio = 1 - ((animation_step - animation_max_steps // 2) / (animation_max_steps // 2))
                    move_y = -self.attack_move_distance_vertical * move_ratio
                    move_x = -self.attack_move_distance_horizontal * move_ratio
            
            rect = pygame.Rect(x + move_x, y + move_y, self.card_width, self.card_height)
            
            bg_color = c.WHITE  
            if animation_in_progress:
                if is_cleave_attack:
                    if target_index_right is not None:
                        if i in (target_index_right - 1, target_index_right, target_index_right + 1):
                            bg_color = c.RED
                else:
                    if current_target is not None and minion == current_target:
                        bg_color = c.RED
            
            pygame.draw.rect(screen, bg_color, rect)
            pygame.draw.rect(screen, c.BLACK, rect, 2)
            
            name_surface = font.render(minion.name, True, c.BLACK)
            name_rect = name_surface.get_rect(center=(rect.centerx, rect.centery - 25))
            screen.blit(name_surface, name_rect)
            
            hp_surface = font.render(f"HP: {minion.health}", True, c.GREEN)
            hp_rect = hp_surface.get_rect(center=(rect.centerx, rect.centery + 25))
            screen.blit(hp_surface, hp_rect)
            
            atk_surface = font.render(f"ATK: {minion.attack}", True, c.RED)
            atk_rect = atk_surface.get_rect(center=(rect.centerx, rect.centery))
            screen.blit(atk_surface, atk_rect)
            
            # 新增：显示护盾信息
            if minion.has_divine_shield():
                shield_surface = font.render("Shield", True, c.BLUE)
                shield_rect = shield_surface.get_rect()
                shield_rect.topright = (rect.right - 5, rect.top + 5)
                screen.blit(shield_surface, shield_rect)
