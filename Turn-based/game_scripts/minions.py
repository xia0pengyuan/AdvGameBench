import constants as c

class Minion:
    def __init__(self, name, cost, attack, health, element, abilities, tier="Bronze"):
        self.name = name
        self.element = element
        self.abilities = abilities
        self.tier = tier
        
        self.cost = cost
        self.base_attack = attack
        self.base_health = health
        
        # 应用tier加成
        self.apply_tier_bonus()
        
        # 燃烧效果
        self.burn_effect = 0
        
        # 用于跟踪死亡处理状态
        self.death_processed = False

    def apply_tier_bonus(self):
        """应用等级加成"""
        if self.tier == "Gold":
            self.attack = self.base_attack * 2
            self.health = self.base_health * 2
        else:
            self.attack = self.base_attack
            self.health = self.base_health

    def take_damage(self, damage, attacker=None, enemy_team=None, allies=None):
        """受到伤害"""
        # 处理中毒效果
        if attacker and "Poisonous" in attacker.abilities and not self.has_divine_shield():
            self.health = 0
            return self.die(attacker, enemy_team, allies)
        
        # 处理圣盾
        if self.has_divine_shield():
            self.remove_divine_shield(allies)
            return 0
        
        # 正常伤害计算
        actual_damage = self.calculate_damage(damage)
        self.health -= actual_damage
        
        # 处理特殊能力
        self.on_damage_taken(attacker)
        
        # 检查是否死亡
        excess = 0
        if self.health <= 0:
            excess = abs(self.health)
            excess = self.die(attacker, enemy_team, allies)
        
        return excess

    def calculate_damage(self, damage):
        """计算实际伤害，子类可以重写以实现护甲等效果"""
        return damage

    def has_divine_shield(self):
        """检查是否有圣盾"""
        return "Divine Shield" in self.abilities

    def remove_divine_shield(self, allies):
        """移除圣盾"""
        if self.has_divine_shield():
            self.abilities.remove("Divine Shield")
            if allies:
                for ally in allies:
                    if ally != self and "Gain Attack on Ally Shield Loss" in ally.abilities:
                        ally.on_ally_shield_loss(self)

    def on_damage_taken(self, attacker):
        """受到伤害后的效果，子类可以重写"""
        pass

    def attack_target(self, target, enemy_team=None, allies=None):
        """攻击目标"""
        # 处理成长效果
        self.handle_growth()
        self.apply_burn()

        total_damage = self.attack 
        excess = target.take_damage(total_damage, attacker=self, enemy_team=allies, allies=enemy_team  )
        
        # 处理特殊攻击效果
        self.on_attack(target, excess, enemy_team, allies)
        
        # 处理反击伤害
        self.take_damage(target.attack, attacker=target, enemy_team=enemy_team , allies=allies)

    def handle_growth(self):
        """处理成长效果，子类可以重写"""
        pass

    def on_attack(self, target, excess, enemy_team, allies):
        """攻击后的效果，子类可以重写"""
        pass

    def die(self, attacker=None, enemy_team=None,allies=None):
        """死亡"""
        
        excess_health = abs(self.health) if self.health < 0 else 0
        
        # 处理死亡后的效果
        self.on_death(attacker, enemy_team, allies)
        
        return excess_health

    def on_death(self, attacker, enemy_minions, allies):
        """死亡后的效果，子类可以重写"""
        pass

    def heal(self, amount):
        """治疗"""
        self.health += amount

    def apply_burn(self):
        """应用燃烧效果"""
        if self.burn_effect > 0:
            self.take_damage(self.burn_effect)
            
    def buff_allies_by_element(self, allies, element, attack_buff, health_buff):
        """为特定元素的友军提供增益"""
        for ally in allies:
            if ally != self and ally.element == element:
                ally.attack += attack_buff
                ally.health += health_buff

    def buff_all_allies(self, allies, attack_buff, health_buff):
        """为所有友军提供增益"""
        for ally in allies:
            if ally != self:
                ally.attack += attack_buff
                ally.health += health_buff
#Invader
class FireLizard(Minion):
    def __init__(self, tier="Bronze"):
        super().__init__(
            name=c.FIRE_LIZARD,
            cost=1,
            attack=2,
            health=2,
            element="Fire",
            abilities=["Deathrattle"],
            tier=tier
        )

    def on_death(self, attacker, enemy_minions, allies):
        """死亡时造成伤害"""
        if attacker and "Deathrattle" in self.abilities:
            damage = 2
            if self.tier == "Gold":
                damage = 4
            attacker.take_damage(damage, attacker=self)

class WaterElemental(Minion):
    def __init__(self, tier="Bronze"):
        super().__init__(
            name=c.WATER_ELEMENTAL,
            cost=1,
            attack=2,
            health=2,
            element="Water",
            abilities=["Growth"],
            tier=tier
        )
        self.growth_value = 1

    def handle_growth(self):
        """处理攻击力成长"""
        value = self.growth_value
        if self.tier == "Gold":
            value *= 2
        self.attack += value

class MoltenHound(Minion):
    def __init__(self, tier="Bronze"):
        super().__init__(
            name=c.MOLTEN_HOUND,
            cost=2,
            attack=3,
            health=1,
            element="Fire",
            abilities=["Deathrattle"],  
            tier=tier
        )

        self.deathrattle_damage = 1
        if self.tier == "Gold":
            self.deathrattle_damage = 2

    def on_death(self, attacker, enemy_team, allies):
        for enemy in enemy_team:
            enemy.take_damage(self.deathrattle_damage, attacker=self)

class PoisonFrog(Minion):
    def __init__(self, tier="Bronze"):
        super().__init__(
            name=c.POISON_FROG,
            cost=2,
            attack=1,
            health=1,
            element="Water",
            abilities=["Poisonous"],
            tier=tier
        )
        
class BattleFrenzy(Minion):
    def __init__(self, tier="Bronze"):
        super().__init__(
            name=c.BATTLE_FRENZY,
            cost=2,
            attack=7,
            health=4,
            element="Guardian",
            abilities=["Battle Frenzy"],
            tier=tier
        )

    def on_attack(self, target, excess, enemy_team, allies):
        attack_reduction = 4
        if self.tier == "Gold":
            attack_reduction = 8
        target.take_damage(self.attack, attacker=self)
        self.attack = max(self.attack - attack_reduction, 0)

class LavaGolem(Minion):
    def __init__(self, tier="Bronze"):
        super().__init__(
            name=c.LAVA_GOLEM,
            cost=3,
            attack=1,
            health=8,
            element="Fire",
            abilities=["Taunt"],
            tier=tier
        )
        self.base_burn_on_attack = 3
        self.burn_on_attack = self.base_burn_on_attack
        if self.tier == "Gold":
            self.burn_on_attack *= 2

    def take_damage(self, damage,  attacker=None, enemy_team=None, allies=None):
        excess = super().take_damage(damage, attacker)
        if attacker:
            attacker.burn_effect = self.burn_on_attack
        return excess

    
class TideGuardian(Minion):
    def __init__(self, tier="Bronze"):
        super().__init__(
            name=c.TIDE_GUARDIAN,
            cost=3,
            attack=4,
            health=2,
            element="Water",
            abilities=["Divine Shield", "Double Strike"],
            tier=tier
        )

    def on_attack(self, target, excess, enemy_team, allies):
        if "Double Strike" in self.abilities:
            total_damage = self.attack  
            target.take_damage(total_damage, attacker=self)

class BanditLeader(Minion):
    def __init__(self, tier="Bronze"):
        super().__init__(
            name=c.BANDIT_LEADER,
            cost=3,
            attack=8,
            health=3,
            element="Rogue",
            abilities=["Excess Damage Carryover"],
            tier=tier
        )
    
    def on_attack(self, target, excess, enemy_team, allies):
        """攻击后将过量伤害传递给下一个敌方随从"""
        if "Excess Damage Carryover" in self.abilities and excess > 0 and enemy_team:
            alive_enemies = enemy_team.get_alive() if hasattr(enemy_team, "get_alive") else enemy_team
            for enemy in alive_enemies:
                if enemy != target:
                    enemy.take_damage(excess, attacker=self)
                    break

class TideLord(Minion):
    def __init__(self, tier="Bronze"):
        super().__init__(
            name=c.TIDE_LORD,
            cost=4,
            attack=4,
            health=10,
            element="Water",
            abilities=["Berserk"],
            tier=tier
        )
    
    def on_damage_taken(self, attacker):
        self.attack *= 2


class Phoenix(Minion):
    def __init__(self, tier="Bronze"):
        super().__init__(
            name=c.PHOENIX,
            cost=4,
            attack=5,
            health=5,
            element="Fire",
            abilities=["Cleave", "Rebirth"],
            tier=tier
        )
    
    def on_attack(self, target, excess, enemy_team, allies):
        if "Cleave" in self.abilities and enemy_team:
            # 如果 enemy_team 有 get_alive 方法，则调用它，否则直接认为 enemy_team 是可迭代对象
            alive_enemies = enemy_team.get_alive() if hasattr(enemy_team, "get_alive") else enemy_team
            for enemy in alive_enemies:
                if enemy != target:
                    total_damage = self.attack 
                    enemy.take_damage(total_damage, attacker=self)

    def on_death(self, attacker, enemy_minions, allies):
        if "Rebirth" in self.abilities:
            self.abilities.remove("Rebirth")
            self.health = self.base_health 
            if self.tier == "Gold":
                self.health = self.base_health
            return 0
        return abs(self.health) if self.health < 0 else 0

class ShadowOverlord(Minion):
    def __init__(self, tier="Bronze"):
        super().__init__(
            name=c.SHADOW_OVERLORD,
            cost=4,
            attack=4,
            health=4,
            element="Rogue",
            abilities=["Deathrattle"],
            tier=tier
        )
        self.death_processed = False
    
        

class SkeletonMinion(Minion):
    def __init__(self, tier="Bronze"):
        super().__init__(
            cost=5,
            attack=3,
            health=1,
            element="Rogue",
            name=c.SKELETON_MINION,
            abilities=[None],
            tier=tier
        )

            

#defender
class Sapling(Minion):
    def __init__(self, tier="Bronze"):
        super().__init__(
            name=c.SAPLING,
            cost=1,
            attack=2,
            health=2,
            element="Nature",
            abilities=["Growth"],
            tier=tier
        )
        self.growth_value = 1

    def handle_growth(self):
        value = self.growth_value
        if self.tier == "Gold":
            value *= 2
        self.health += value


class RockBeetle(Minion):
    def __init__(self, tier="Bronze"):
        super().__init__(
            name=c.ROCK_BEETLE,
            cost=1,
            attack=1,
            health=5,
            element="Earth",
            abilities=["Taunt"],
            tier=tier
        )


class ForestSeer(Minion):
    def __init__(self, tier="Bronze"):
        super().__init__(
            name=c.FOREST_SEER,
            cost=2,
            attack=1,
            health=2,
            element="Nature",
            abilities=["Buff Nature Allies"],
            tier=tier
        )

    def on_game_start(self, allies):
        if allies:
            attack_buff = 1
            health_buff = 1
            if self.tier == "Gold":
                attack_buff = 2
                health_buff = 2
            self.buff_allies_by_element(allies, "Nature", attack_buff, health_buff)

class StoneWarrior(Minion):
    def __init__(self, tier="Bronze"):
        super().__init__(
            name=c.STONE_WARRIOR,
            cost=2,
            attack=2,
            health=5,
            element="Earth",
            abilities=["Taunt","Deathrattle"],
            tier=tier
        )
        self.death_processed = False



class EliteSoldier(Minion):
    def __init__(self, tier="Bronze"):
        super().__init__(
            name=c.ELITE_SOLDIER,
            cost=2,
            attack=1,
            health=1,
            element="Guardian",
            abilities=["Inspire"],  
            tier=tier
        )

    def on_game_start(self, allies):

        index = allies.index(self)
        
        if index > 0:
            left_ally = allies[index - 1]
            if "Divine Shield" not in left_ally.abilities:
                left_ally.abilities.append("Divine Shield")
            left_ally.attack += 1
        
        if index < len(allies) - 1:
            right_ally = allies[index + 1]
            if "Divine Shield" not in right_ally.abilities:
                right_ally.abilities.append("Divine Shield")
            right_ally.attack += 1


class VineProtector(Minion):
    def __init__(self, tier="Bronze"):
        super().__init__(
            name=c.VINE_PROTECTOR,
            cost=3,
            attack=3,
            health=4,
            element="Nature",
            abilities=["Heal on Attacked"],
            tier=tier
        )

    def on_damage_taken(self, attacker):
        if "Heal on Attacked" in self.abilities:
            heal_amount = 2
            if self.tier == "Gold":
                heal_amount *= 2
            self.heal(heal_amount)


class BlackRock(Minion):
    def __init__(self, tier="Bronze"):
        super().__init__(
            name=c.BLACK_ROCK,
            cost=3,
            attack=2,
            health=1,
            element="Earth",
            abilities=["Gain Health on Game Start"],
            tier=tier
        )

    def on_game_start(self, allies):
        heal_amount = 3 * (len(allies)-1) 
        self.heal(heal_amount)


class Paladin(Minion):
    def __init__(self, tier="Bronze"):
        super().__init__(
            name=c.PALADIN,
            cost=3,
            attack=3,
            health=6,
            element="Guardian",
            abilities=["Divine Shield", "Gain Attack on Ally Shield Loss"],
            tier=tier
        )

    def on_ally_shield_loss(self, ally):
        self.attack += 2


class AncientTreant(Minion):
    def __init__(self, tier="Bronze"):
        super().__init__(
            name=c.ANCIENT_TREANT,
            cost=4,
            attack=2,
            health=3,
            element="Nature",
            abilities=["Empowered Buff Nature Allies"],
            tier=tier
        )
    
    def on_game_start(self, allies):
        if allies:
            attack_buff = 2
            health_buff = 2
            if self.tier == "Gold":
                attack_buff = 4
                health_buff = 4
            self.buff_all_allies(allies, attack_buff, health_buff)

class King(Minion):
    def __init__(self, tier="Bronze"):
        super().__init__(
            name=c.KING,
            cost=4,
            attack=3,
            health=12,
            element="Guardian",
            abilities=["Summon Shielded Soldier on Attack"],
            tier=tier
        )
    
    def on_attack(self, target, excess, enemy_team, allies):

        MAX_ALLIES = 5  
        if len(allies) < MAX_ALLIES:
            soldier = Minion(
                name="Soldier",
                cost=0,
                attack=1,
                health=1,
                element="Guardian",
                abilities=["Divine Shield"],
                tier="Bronze"
            )
            allies.append(soldier)




class MountainGiant(Minion):
    def __init__(self, tier="Bronze"):
        super().__init__(
            name=c.MOUNTAIN_GIANT,
            cost=4,
            attack=4,
            health=9,
            element="Earth",
            abilities=["Taunt"],
            tier=tier
        )
        self.base_attack_reduction = 2
        self.attack_reduction = self.base_attack_reduction
        if self.tier == "Gold":
            self.attack_reduction *= 2

    def take_damage(self, damage, attacker=None, enemy_team=None, allies=None):
        excess = super().take_damage(damage, attacker)
        if attacker:
            attacker.attack = max(attacker.attack - self.attack_reduction, 0)
        return excess