import random
import math
from datetime import date

from Stat import Stat

class Avatar:
    """ General class """
    id = 0

    def __init__(self, targs):
        self._nom = targs['name']
        self._race = targs['race']
        self._classe = targs['classe']
        self._bag = targs['bag']
        self._equipment = targs['equipment']
        self._element = targs['element']
        self._lvl = 1
        self._stat = Stat({
            'strength': 1, 
            'magic': 1,
            'agility': 1,
            'speed': 1,
            'charisma': 0,
            'chance': 0
        })
        Avatar.id += 1
        self._id = Avatar.id
        self.sumStat()
        self._life = self._stat.life_point
        self._statistics = {"fight": 0, "win": 0, "maxDamage": 0}

    def getBag(self):
        return self._bag._lItems

    def initiative(self):
        min_val = self._stat.speed
        max_val = self._stat.agility + self._stat.chance + self._stat.speed
        return random.randint(min_val, max_val)

    def damages(self):
        critique = random.randint(0, self._stat.chance)
        min_val = 0
        max_val = self._stat.attack

        if critique > self._stat.chance / 2:
            print("Full damages")
            max_damage = random.randint(max_val, 2 * max_val)
        else:
            max_damage = random.randint(min_val, max_val)
        print(f"{self._nom} done {max_damage}")
        return max_damage
    
    
    def defense(self, v):
        damage = v  # Dégâts initiaux
        min_val = self._stat.agility
        max_val = self._stat.agility + self._stat.chance + self._stat.speed
        duck = random.randint(min_val, max_val)

        if duck == max_val:
            print("The shot is dodged")
            damage = 0  # Aucun dégât
        elif duck > max_val / 2:
            print("Partial dodge")
            damage /= 2  # Dégâts réduits

        #damage -= self._stat.defense  # Réduction des dégâts par la défense
       # if damage < 0:
        #    damage = 0

        self._life -= damage  # Applique les dégâts à la vie
        print("---------------------------------------------------------------------------"+ "Héros : "+ self._nom +" PV = " + str(self._life) + " Damage = " + str(damage))
        if self._life < 0:
            self._life = 0

        print(f"Life point: {self._life} / {self._stat.life_point}")

        def __str__(self):
            return str(self._nom)

    def sumStat(self):
        equipment_bonus = 0
        for stat_name in self._stat.__dict__:
            for item in self._equipment:
                equipment_bonus += item._stat.__dict__[stat_name]
            self._stat.__dict__[stat_name] = self._race._stat.__dict__[stat_name] + self._classe._stat.__dict__[stat_name] + equipment_bonus
