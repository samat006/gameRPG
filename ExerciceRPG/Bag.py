class Bag:
    def __init__(self, attributes):
        # Vérifiez que 'sizeMax' et 'items' sont bien dans le dictionnaire 'attributes'
        self.sizeMax = attributes.get('sizeMax', 0)  # Valeur par défaut 0 si pas fourni
        self.items = attributes.get('items', [])  # Assurez-vous que 'items' est une liste vide par défaut

    def addItem(self, item):
        if self._size < self._sizeMax:
            self._lItems.append(item)
            self._size += 1
            return True
        else:
            print("Le sac est plein, impossible d'ajouter un nouvel item.")
            return False

    def reset(self):
        """Vide le contenu du sac."""
        self._lItems = []
        self._size = 0

    def __str__(self):
        if not self._lItems:
            return "Le sac est vide."
        return "Contenu du sac : " + ", ".join(item._name for item in self._lItems)

