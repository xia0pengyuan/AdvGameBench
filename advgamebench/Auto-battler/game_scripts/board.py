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
        
        self.top_team_y = c.SCREEN_HEIGHT // 2 - self.middle_gap // 2 - self.card_height
        self.bottom_team_y = c.SCREEN_HEIGHT // 2 + self.middle_gap // 2
        
        self.attack_move_distance_vertical = 15
        self.attack_move_distance_horizontal = 30  

    def draw(self, screen, font, current_attacker=None, current_target=None, 
             animation_in_progress=False, animation_step=0, animation_max_steps=0,
             attacker_team=None, defender_team=None):
        pygame.draw.line(screen, c.BLACK, 
                         (0, c.SCREEN_HEIGHT // 2), 
                         (c.SCREEN_WIDTH, c.SCREEN_HEIGHT // 2), 
                         2)

        is_cleave_attack = False
        if current_attacker is not None:
            if [att for att in [current_attacker] if "Cleave" in getattr(att, "abilities", [])]:
                is_cleave_attack = True

        target_index_left = None
        if animation_in_progress and current_target and current_target in self.team_left.minions:
            target_index_left = self.team_left.minions.index(current_target)

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
            
            bg_color = (230, 230, 230)
            if animation_in_progress:
                if is_cleave_attack:
                    if target_index_left is not None:
                        if i in (target_index_left - 1, target_index_left, target_index_left + 1):
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
            hp_rect = hp_surface.get_rect(center=(rect.centerx, rect.centery))
            screen.blit(hp_surface, hp_rect)
            
            atk_surface = font.render(f"ATK: {minion.attack}", True, c.RED)
            atk_rect = atk_surface.get_rect(center=(rect.centerx, rect.centery + 25))
            screen.blit(atk_surface, atk_rect)
            
            if minion.has_divine_shield():
                shield_surface = font.render("Shield", True, c.BLUE)
                shield_rect = shield_surface.get_rect()
                shield_rect.topright = (rect.right - 5, rect.top + 5)
                screen.blit(shield_surface, shield_rect)
        
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
            
            if minion.has_divine_shield():
                shield_surface = font.render("Shield", True, c.BLUE)
                shield_rect = shield_surface.get_rect()
                shield_rect.topright = (rect.right - 5, rect.top + 5)
                screen.blit(shield_surface, shield_rect)
