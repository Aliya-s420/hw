from random import randint, choice


class GameEntity:
    def __init__(self, name, health, damage):
        self.__name = name
        self.__health = health
        self.__damage = damage

    @property
    def name(self):
        return self.__name

    @property
    def health(self):
        return self.__health

    @health.setter
    def health(self, value):
        if value < 0:
            self.__health = 0
        else:
            self.__health = value

    @property
    def damage(self):
        return self.__damage

    @damage.setter
    def damage(self, value):
        self.__damage = value

    def __str__(self):
        return f'{self.__name} health: {self.health} damage: {self.damage}'


class Boss(GameEntity):
    def __init__(self, name, health, damage):
        super().__init__(name, health, damage)
        self.__defence = None

    @property
    def defence(self):
        return self.__defence

    def choose_defence(self, heroes: list):
        hero: Hero = choice(heroes)
        self.__defence = hero.ability

    def attack(self, heroes: list):
        for hero in heroes:
            if hero.health > 0:
                if type(hero) == Berserk and self.defence != hero.ability:
                    hero.blocked_damage = choice([5, 10])
                    hero.health -= (self.damage - hero.blocked_damage)
                else:
                    hero.health -= self.damage

    def __str__(self):
        return 'BOSS ' + super().__str__() + f' defence: {self.__defence}'


class Hero(GameEntity):
    def __init__(self, name, health, damage, ability):
        super().__init__(name, health, damage)
        self.__ability = ability

    @property
    def ability(self):
        return self.__ability

    def attack(self, boss: Boss):
        boss.health -= self.damage

    def apply_super_power(self, boss: Boss, heroes: list):
        pass


class Warrior(Hero):
    def __init__(self, name, health, damage):
        super().__init__(name, health, damage, 'CRITICAL_DAMAGE')

    def apply_super_power(self, boss: Boss, heroes: list):
        crit = randint(2, 5) * self.damage
        boss.health -= crit
        print(f'Warrior {self.name} hit critically {crit}')


class Witcher(Hero):
    def __init__(self, name, health, damage):
        super().__init__(name, health, damage, 'SACRIFICE')
        self.used_power = False

    def attack(self, boss: Boss):
        pass

    def apply_super_power(self, boss: Boss, heroes: list):
        if not self.used_power:
            for hero in heroes:
                if hero.health <= 0 and hero != self:
                    hero.health = self.health
                    self.health = 0
                    self.used_power = True
                    print(f'Witcher {self.name} sacrificed to revive {hero.name}')
                    break


class Magic(Hero):
    def __init__(self, name, health, damage, boost_amount):
        super().__init__(name, health, damage, 'BOOST')
        self.__boost_amount = boost_amount

    def apply_super_power(self, boss: Boss, heroes: list):
        if round_number <= 4:
            for hero in heroes:
                if hero.health > 0 and hero != self:
                    hero.damage += self.__boost_amount
            print(f'Magic {self.name} boosted aal heroes by {self.__boost_amount}')


class Healer(Hero):
    def __init__(self, name, health, damage, heal_points):
        super().__init__(name, health, damage, 'HEAL')
        self.__heal_points = heal_points

    def apply_super_power(self, boss: Boss, heroes: list):
        for hero in heroes:
            if hero.health > 0 and hero != self:
                hero.health += self.__heal_points


class Berserk(Hero):
    def __init__(self, name, health, damage):
        super().__init__(name, health, damage, 'BLOCK_REVERT')
        self.__blocked_damage = 0

    @property
    def blocked_damage(self):
        return self.__blocked_damage

    @blocked_damage.setter
    def blocked_damage(self, value):
        self.__blocked_damage = value

    def apply_super_power(self, boss: Boss, heroes: list):
        boss.health -= self.blocked_damage
        print(f'Berserk {self.name} reverted {self.blocked_damage} damage to boss.')


class Hacker(Hero):
    def __init__(self, name, health, damage, steal_amount):
        super().__init__(name, health, damage, 'STEAL_HEALTH')
        self.round_to_act = 0
        self.__steal_amount = steal_amount

    def apply_super_power(self, boss: Boss, heroes: list):
        if round_number % 2 == 0 and boss.health > self.__steal_amount:
            boss.health -= self.__steal_amount
            target = choice([hero for hero in heroes if hero.health > 0 and hero != self])
            target.health += self.__steal_amount
            print(f'Hacker {self.name} stole {self.__steal_amount} health from Boss and gave it to {target.name}')


class Golem(Hero):
    def __init__(self, name, health, damage):
        super().__init__(name, health, damage, 'DAMAGE_TANK')

    def apply_super_power(self, boss: Boss, heroes: list):
        for hero in heroes:
            if hero != self and hero.health > 0:
                absorb = boss.damage // 5
                self.health -= absorb
                hero.health += absorb
        print(f'Golem {self.name} absorbed damage for the team')


class Avrora(Hero):
    def __init__(self, name, health, damage):
        super().__init__(name, health, damage, 'INVISIBLE')
        self.invisible_rounds = 0
        self.can_use_power = True
        self.saved_damage = 0

    def apply_super_power(self, boss: Boss, heroes: list):
        if self.can_use_power:
            self.invisible_rounds = 2
            self.can_use_power = False
            print(f'Avrora {self.name} becomes invisible!')

    def take_damage(self, damage):
        if self.invisible_rounds > 0:
            self.saved_damage += damage
            return 0
        return damage

    def attack(self, boss: Boss):
        if self.invisible_rounds == 0 and self.saved_damage > 0:
            boss.health -= self.saved_damage
            print(f'Avrora {self.name} returns {self.saved_damage} damage to Boss!')
            self.saved_damage = 0
        super().attack(boss)


round_number = 0


def play_round(boss: Boss, heroes: list):
    global round_number
    round_number += 1
    boss.choose_defence(heroes)
    boss.attack(heroes)
    for hero in heroes:
        if hero.health > 0 and boss.health > 0 and boss.defence != hero.ability:
            hero.attack(boss)
            hero.apply_super_power(boss, heroes)
    show_statistics(boss, heroes)


def is_game_over(boss: Boss, heroes: list):
    if boss.health <= 0:
        print('Heroes won!!!')
        return True
    all_heroes_dead = True
    for hero in heroes:
        if hero.health > 0:
            all_heroes_dead = False
            break
    if all_heroes_dead:
        print('Boss won!!!')
        return True
    return False


def start_game():
    boss = Boss('Fuse', 1000, 50)

    warrior_1 = Warrior('Anton', 280, 10)
    warrior_2 = Warrior('Akakii', 270, 15)
    magic = Magic('Itachi', 290, 10, 5)
    doc = Healer('Aibolit', 250, 5, 15)
    assistant = Healer('Dulittle', 300, 5, 5)
    berserk = Berserk('Guts', 260, 10)
    witcher = Witcher('Tom', 240, 10)
    hacker = Hacker('Sasha', 240, 15, 2)
    golem = Golem('Artur', 240, 15)
    avrora = Avrora('Moon', 230, 15)


    heroes_list = [warrior_1, doc, warrior_2, magic, berserk, assistant, witcher, hacker, golem, avrora]

    show_statistics(boss, heroes_list)
    while not is_game_over(boss, heroes_list):
        play_round(boss, heroes_list)


def show_statistics(boss: Boss, heroes: list):
    print(f'ROUND {round_number} -----------------')
    print(boss)
    for hero in heroes:
        print(hero)


start_game()
