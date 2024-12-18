from datetime import date
import math

from Avatar import Avatar


class Hero:
    def __init__(self, attributes):  # Vérifiez que vous recevez bien 'attributes' comme argument
        self._nom = attributes.get('name')  # Utilisation de 'attributes' pour récupérer les valeurs
        self._life = attributes.get('life')
        self._bag = attributes.get('bag')
        self._position = attributes.get('position')

    def to_dict(self):
        return {
            'name': self._nom,  # Accédez à _nom dans la méthode to_dict()
            'life': self._life,
            'bag': [item.to_dict() for item in self._bag.items],  # Si bag contient des objets Item
            'position': self._position
        }


    def lvl(self):
        level = math.floor(self._xp / 100)
        if level < 1:
            level = 1

        if level > self._lvl:
            print("### New level ###")
            self.newLvl()
        return level

    def newLvl(self):
        for stat_name in self._stat.__dict__:
            self._stat.__dict__[stat_name] += 5
        self._life = self._stat.life_point
        print("### Stats upgraded ###")

    def setXP(self, xp):
        self._xp += xp
        self._lvl = self.lvl()

    def __str__(self):
        return f"Joueur {self._nom} de niveau {self._lvl}, classe {self._classe}, race {self._race}"

    def getBag(self):
        return self.bag

    def save(self):
        file_name = f"{date.today()}_{Hero.id}_{self._nom}.txt"
        with open(file_name, "w+") as f:
            f.write(f"{self._nom}\n{self._race._name}\n{self._classe._name}\n")
            f.write(f"Lvl: {self._lvl}\nXP: {self._xp}\n")
            for stat_name, stat_value in self._stat.__dict__.items():
                f.write(f"{stat_name} {stat_value}\n")
            for item in self._equipment:
                f.write(f"{item}\n")
            for item in self.bag:  # Utilisation directe de self.bag
                f.write(f"{item}\n")

    def saveXML(self):
        file_name = f"{date.today()}_{Hero.id}_{self._nom}.xml"
        with open(file_name, "w+") as f:
            xml = "<?xml version='1.0' encoding='UTF-8'?>"
            xml += f"<avatar id='{Hero.id}'>"
            xml += f"<name>{self._nom}</name><race>{self._race._name}</race>"
            xml += f"<level>{self._classe._name}</level><xp>{self._lvl}</xp><name>{self._xp}</name>"
            xml += "<stats>"
            for stat_name, stat_value in self._stat.__dict__.items():
                xml += f"<{stat_name}>{stat_value}</{stat_name}>"
            xml += "</stats><equipments>"
            for i, item in enumerate(self._equipment, start=1):
                xml += f"<item_{i}>{item._name}</item_{i}>"
            xml += "</equipments><bag>"
            for i, item in enumerate(self.bag, start=1):  # Utilisation directe de self.bag
                xml += f"<item_{i}>{item._name}</item_{i}>"
            xml += "</bag></avatar>"
            f.write(xml)

    @staticmethod
    def load():
        pass

 