from status import Status

class Skill:
    def __init__(self, name, power, element):
        self.name = name      # Skill name
        self.power = power    # Base power of the skill
        self.element = element  # Element of the skill (e.g. Fire, Wood, etc.)

    def __str__(self):
        return f"{self.name}({self.power})"


class Character:
    def __init__(self, name, element, skills):
        self.name = name
        self.element = element  
        self.max_hp = 999999
        self.hp = 100
        self.skills = skills  
        self.skill_index = 0  
        self.statuses = {}

        self.stored_damage = 0

    def add_status(self, status):
        """
        Apply a new status effect to this character.

        Raises:
            ValueError: If the provided object is not a Status instance.
        """
        if not isinstance(status, Status):
            raise ValueError("Status must be an instance of Status class")
        if status.name in self.statuses:
            self.statuses[status.name].append(status)
        else:
            self.statuses[status.name] = [status]

    def remove_status(self, status_name):
        if status_name in self.statuses:
            del self.statuses[status_name]

    def update_statuses(self):
        """
        Decrement duration of each status at end of turn and remove expired ones.
        """
        for name in list(self.statuses.keys()):
            new_list = []
            for s in self.statuses[name]:
                s.duration -= 1
                if s.duration > 0:
                    new_list.append(s)
            if new_list:
                self.statuses[name] = new_list
            else:
                del self.statuses[name]

    def process_statuses(self):
        """
        Apply ongoing effects for each status (e.g., burn damage, regen).
        """
        for status_list in self.statuses.values():
            for s in status_list:
                s.process(self)

    def get_status_layers(self, status_name):
        """
        Return the total layers of the specified status.
        """
        if status_name in self.statuses:
            return sum(s.layers for s in self.statuses[status_name])
        return 0

    def get_next_skill(self):
        """
        Simple round-robin skill index.
        """
        skill = self.skills[self.skill_index]
        self.skill_index = (self.skill_index + 1) % len(self.skills)
        return skill

    def is_alive(self):
        return self.hp > 0

    def reset(self):
        """
        Reset character state for multiple rounds of testing.
        """
        self.hp = self.max_hp
        self.skill_index = 0
        self.statuses = {}
        self.stored_damage = 0

    def __str__(self):
        return f"{self.name}({self.element}) HP:{self.hp}"

    def attack(attacker, defender, skill_func):
        # 1. Save HP before attack
        defender_hp_before = defender.hp
        # 2. Perform the skill action
        skill_func(attacker, defender)
        # 3. Compute net damage dealt
        damage_dealt = max(0, defender_hp_before - defender.hp)  

        for status_list in defender.statuses.values():
            for status_obj in status_list:
                reflect = status_obj.get_reflect_damage(damage_dealt)
                if reflect > 0:
                    attacker.hp -= reflect

        for status_list in attacker.statuses.values():
            for status_obj in status_list:
                counter = status_obj.get_counter_damage()
                if counter > 0:
                    attacker.hp -= counter

        if "Faith Emblem" in defender.statuses:
            defender.remove_status("Faith Emblem")
        if "Divine Link" in defender.statuses:
            defender.remove_status("Divine Link")
