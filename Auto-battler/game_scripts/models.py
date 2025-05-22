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
        # 用字典存储状态，key=状态名，value=【列表】(可以堆叠多个相同名字的状态)
        self.statuses = {}

        # 可选的：有些技能会储存伤害，用作二次结算
        self.stored_damage = 0

    def add_status(self, status):
        if not isinstance(status, Status):
            raise ValueError("状态对象必须是 Status 类的实例")
        if status.name in self.statuses:
            self.statuses[status.name].append(status)
        else:
            self.statuses[status.name] = [status]

    def remove_status(self, status_name):
        if status_name in self.statuses:
            del self.statuses[status_name]

    def update_statuses(self):
        """
        每回合结束时更新所有状态的持续时间，并移除到期状态
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
        每回合处理所有状态的持续效果（如燃烧持续伤害、持续治疗、毒伤等）
        """
        for status_list in self.statuses.values():
            for s in status_list:
                s.process(self)

    def get_status_layers(self, status_name):
        """
        返回指定状态的累计层数
        """
        if status_name in self.statuses:
            return sum(s.layers for s in self.statuses[status_name])
        return 0

    def get_next_skill(self):
        """
        简单的轮转技能索引
        """
        skill = self.skills[self.skill_index]
        self.skill_index = (self.skill_index + 1) % len(self.skills)
        return skill

    def is_alive(self):
        return self.hp > 0

    def reset(self):
        """
        重置角色状态，方便进行多次对局测试
        """
        self.hp = self.max_hp
        self.skill_index = 0
        self.statuses = {}
        self.stored_damage = 0

    def __str__(self):
        return f"{self.name}({self.element}) HP:{self.hp}"

    def attack(attacker, defender, skill_func):

        defender_hp_before = defender.hp

        skill_func(attacker, defender)

        damage_dealt = max(0, defender_hp_before - defender.hp)  # 计算本次技能对 defender 实际造成的伤害

        for status_list in defender.statuses.values():
            for status_obj in status_list:
                reflect = status_obj.get_reflect_damage(damage_dealt)
                if reflect > 0:
                    attacker.hp -= reflect

        # 4. attacker 自身状态的额外反击伤害
        for status_list in attacker.statuses.values():
            for status_obj in status_list:
                counter = status_obj.get_counter_damage()
                if counter > 0:
                    attacker.hp -= counter

        # 5. 清除一次性触发的状态
        if "Faith Emblem" in defender.statuses:
            defender.remove_status("Faith Emblem")
        if "Divine Link" in defender.statuses:
            defender.remove_status("Divine Link")
