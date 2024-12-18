# Classe.py
from Stat import Stat

class Classe:
    def __init__(self, name):
        self._name = name
        self._stat = Stat({
            'strength': 4, 
            'magic': 2,
            'agility': 5,
            'speed': 3,
            'charisma': 2,
            'chance': 1
        })
    
    def __str__(self):
        return self._name
