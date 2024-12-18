class Item:
    """Classe représentant un objet dans le jeu"""
    nbr = 0

    def __init__(self, targs, stat):
        self._name = targs['name']
        self._type = targs['type']
        self._space = targs['space']
        self._stat = stat
        self._position = targs.get('position', None)  # Position de l'objet, défaut à None

        Item.nbr += 1

    @property
    def name(self):
        return self._name

    @property
    def type(self):
        return self._type

    @property
    def space(self):
        return self._space

    @property
    def stats(self):
        return self._stat

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, value):
        self._position = value  # Permet de mettre à jour la position de l'objet

    def __str__(self):
        return self._name
    
    def to_dict(self):
        return {
            'name': self.name,
            'type': self.type,
            'space': self.space,
            'stats': self.stats,
            'position': self.position  # Ajouter la position à la sortie du dictionnaire
        }
