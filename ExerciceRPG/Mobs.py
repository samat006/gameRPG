import random
from Avatar import Avatar
from Stat import Stat

class Mobs(Avatar):
    def __init__(self, targs):
        super().__init__(targs)
        self._type = targs["type"]
        self._initial_life = targs.get("life", 100)
        self._life = self._initial_life
        self._nom = targs["name"]  # Assurez-vous que le nom est défini ici
        self._position = None  # Ajouter position

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, value):
        self._position = value

    def __str__(self):
        return f"Mobs {self._type} {self._nom}, PV: {self._life}, Position: {self._position}"

    def to_dict(self):
        return {
            'name': self._nom,  # Utiliser _nom ici au lieu de name
            'type': self._type,
            'life': self._life,
            'position': self._position  # Inclure la position
        }

    @property
    def life(self):
        return self._life

    @life.setter
    def life(self, value):
        self._life = value

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, value):
        self._position = value  # Permet de mettre à jour la position du mob

    def reset(self):
        self._life = self._initial_life  

    def __str__(self):
        return f"Mobs {self._type} {self._nom}, PV: {self._life}, Position: {self._position}"

    def to_dict(self):
        return {
            'name': self._nom,  # Utiliser _nom ici
            'type': self._type,  # Utilisez _type pour récupérer le type
            'race': self.race.name,
            'classe': self.classe.name,
            'element': self.element,
            'life': self.life,
            'position': self.position  # Ajouter la position dans le dictionnaire retourné
        }
