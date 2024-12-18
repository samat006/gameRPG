from Hero import Hero
from Plateau import jouer
from Race import Race
from Class import Classe
from Mobs import Mobs
from Item import Item
from Bag import Bag

def main():
    race_humain = Race('Humain')
    classe_guerrier = Classe('Guerrier')
    race_elfe = Race('Elfe')
    classe_mage = Classe('Mage')

    nom_joueur1 = input("Entrez le nom du Héros 1 : ")
    nom_joueur2 = input("Entrez le nom du Héros 2 : ")

    bag_joueur1 = Bag({'sizeMax': 3, 'items': []})
    bag_joueur2 = Bag({'sizeMax': 3, 'items': []})

    # Initialisation des joueurs avec les objets Race et Classe
    joueur1 = Hero({
        'name': nom_joueur1,  
        'profession': 'Guerrier',
        'race': race_humain,
        'classe': classe_guerrier,
        'bag': bag_joueur1,
        'equipment': [],  
        'element': 'Feu',
        'life': 100,  
        'position': 0 
    })
    
    joueur2 = Hero({
        'name': nom_joueur2,  
        'profession': 'Mage',
        'race': race_elfe,
        'classe': classe_mage,
        'bag': bag_joueur2,
        'equipment': [], 
        'element': 'Eau',
        'life': 100, 
        'position': 0  
    })

    # Initialisation des mobs avec des sacs
    mobs = [
        Mobs({'name': 'Goblin', 'type': 'Goblin', 'race': race_humain, 'classe': classe_guerrier, 'bag': Bag({'sizeMax': 5, 'items': []}), 'equipment': [], 'element': 'Terre', 'life': 5}),
        Mobs({'name': 'Orc', 'type': 'Orc', 'race': race_elfe, 'classe': classe_mage, 'bag': Bag({'sizeMax': 5, 'items': []}), 'equipment': [], 'element': 'Vent', 'life': 15}),
    ]

    # Initialisation des items disponibles
    items_disponibles = [
        Item({"name": "Épée en fer", "type": "arme", "space": 1}, {"attaque": 10}),
        Item({"name": "Bouclier en bois", "type": "défense", "space": 1}, {"défense": 5}),
        Item({"name": "Potion de soin", "type": "consommable", "space": 1}, {"soin": 20}),
        Item({"name": "Arc", "type": "arme", "space": 1}, {"attaque": 7}),
    ]

    # Lancer la partie en passant les items disponibles
    jouer(joueur1, joueur2, mobs, items_disponibles)

if __name__ == "__main__":
    main()

