class Status:
    def __init__(self, name, duration, layers=1, reflect_damage=0, counter_damage=0,
                 damage_reduction=0, flat_damage_reduction=0, bonus_damage=0, **kwargs):
        self.name = name
        self.duration = duration
        self.layers = layers
        self.reflect_damage = reflect_damage
        self.counter_damage = counter_damage
        self.damage_reduction = damage_reduction  
        self.flat_damage_reduction = flat_damage_reduction 
        self.bonus_damage = bonus_damage  
        self.data = kwargs

    def get_reflect_damage(self, damage_dealt):
        return self.reflect_damage

    def get_counter_damage(self):
        return self.counter_damage

    def get_damage_reduction(self):
        """
        Returns the total damage reduction provided by this status (scaled by layers).
        """
        return self.damage_reduction * self.layers

    def get_flat_damage_reduction(self):
        """
        Returns the total flat damage reduction provided by this status (scaled by layers).
        """
        return self.flat_damage_reduction * self.layers

    def get_bonus_damage(self):
        """
        Returns the bonus damage provided by this status (scaled by layers).
        This value can be added to the character's attack damage.
        """
        return self.bonus_damage * self.layers

    def process(self, target):
        """
        Apply status effects on the target each round.
        """
        # Continuous damage effect
        if "damage_per_round" in self.data and self.data["damage_per_round"] > 0:
            dmg = self.data["damage_per_round"] * self.layers
            target.hp -= dmg

        # Continuous healing effect
        if "heal_per_round" in self.data and self.data["heal_per_round"] > 0:
            heal = self.data["heal_per_round"] * self.layers
            old_hp = target.hp
            target.hp = min(target.max_hp, target.hp + heal)
            actual_heal = target.hp - old_hp

        if self.bonus_damage > 0 and self.data.get("apply_bonus", False):
            bonus_dmg = self.get_bonus_damage()
            target.hp -= bonus_dmg  


