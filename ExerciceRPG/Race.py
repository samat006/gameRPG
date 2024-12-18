from Stat import Stat

class Race:
    def __init__(self, name):
        self._name = name
        self._stat = Stat({
            'strength': 5, 
            'magic': 3,
            'agility': 4,
            'speed': 2,
            'charisma': 1,
            'chance': 1
        })
    
    def __str__(self):
        return self._name
