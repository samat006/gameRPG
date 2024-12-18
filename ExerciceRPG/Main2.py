from flask import Flask, request, jsonify, render_template
from Hero import Hero
from Plateau import jouer,combatPVE
from Race import Race
from Class import Classe
from Mobs import Mobs
from Item import Item
from Bag import Bag
import random

app = Flask(__name__)

# Initialisation des données globales
race_humain = Race('Humain')
classe_guerrier = Classe('Guerrier')
race_elfe = Race('Elfe')
classe_mage = Classe('Mage')


@app.route('/')
def home():
    return render_template('plat.html')



# Route pour créer une nouvelle partie
@app.route('/combat', methods=['POST'])
@app.route('/combat', methods=['POST'])
def combat():
    try:
        # Création des items
        items_disponibles = [
            Item({"name": "Épée en fer", "type": "arme", "space": 1}, {"attaque": 10}),
            Item({"name": "Bouclier en bois", "type": "défense", "space": 1}, {"défense": 5}),
            Item({"name": "Potion de soin", "type": "consommable", "space": 1}, {"soin": 20})
        ]

        # Recevoir les données envoyées par le client
        data = request.get_json()
        print("Données reçues:", data)

        # Reconstruire le joueur et le mob
        # Modification ici pour accéder directement à 'joueur' au lieu de 'joueur 1'
        joueur_data = data.get('joueur')  # Changed from 'joueur 1'
        mob_data = data.get('mob')

        if not joueur_data or not mob_data:
            raise ValueError("Données du joueur ou du mob manquantes")

        joueur = Hero({
            'name': joueur_data.get('name', 'Unknown'),
            'life': joueur_data.get('life', 100),
            'bag': Bag({'sizeMax': 3, 'items': joueur_data.get('bag', [])}),
            'profession': 'Guerrier',  # Valeurs par défaut ajoutées
            'race': race_humain,
            'classe': classe_guerrier,
            'equipment': [],
            'element': 'Feu',
            'position': 0
        })

        mob = Mobs({
            'name': mob_data.get('name', 'Unknown'),
            'life': mob_data.get('hp', 50),  # Changed from 'life' to 'hp'
            'type': mob_data.get('name', 'Unknown'),
            'race': race_humain,
            'classe': classe_guerrier,
            'bag': Bag({'sizeMax': 5, 'items': []}),
            'equipment': [],
            'element': 'Terre'
        })

        # Exécuter le combat
        resultat = combatPVE(joueur, mob, items_disponibles)

        # Retourner les résultats
        return jsonify({
            'logs': resultat.get('logs', []),
            'vainqueur': resultat.get('vainqueur', ''),
            'joueur': {
                'name': joueur._nom,
                'vie_restante': joueur._life,
                'bag': [item.__dict__ for item in joueur.bag.items] if joueur.bag else []
            },
            'mob': {
                'name': mob._nom,
                'vie_restante': mob._life
            },
            'item_gagne': resultat.get('item_gagne', None)
        })

    except Exception as e:
        print("Une erreur s'est produite:", e)
        return jsonify({'error': str(e)}), 500




@app.route('/ajouter-item', methods=['POST'])
def ajouter_item():
    try:
        data = request.get_json()
        joueur = data.get('joueur')  # Identifiez le joueur (par ID ou nom)
        position = data.get('position')  # Position de l'item sur le plateau

        # Exemple : récupérer l'item et l'ajouter au sac du joueur
        item = contenuPlateau[position]
        if item is None or item != "item":
            return jsonify({'error': 'Aucun item trouvé à cette position'}), 400

        # Ajoutez l'item au sac du joueur ici
        joueur['bag'].append(item)

        return jsonify({'item': {'nom': item['name']}})
    except Exception as e:
        return jsonify({'error': str(e)}), 500



@app.route('/plat')
def plat():
    return render_template('plat.html')

# Fonction pour générer des positions aléatoires uniques
def generer_positions(plateau_size, nb_elements):
    return random.sample(range(plateau_size), nb_elements)


# Route pour créer une nouvelle partie
@app.route('/new-game', methods=['POST'])
def new_game():
    try:
        # Recevoir les données envoyées par le client
        data = request.get_json()
        print("Données reçues:", data)

        # Récupérer les noms des joueurs
        nom_joueur1 = data.get('player1_name')
        nom_joueur2 = data.get('player2_name')

        if not nom_joueur1 or not nom_joueur2:
            print("Erreur : Les noms des joueurs sont requis.")
            return jsonify({'error': 'Les noms des joueurs sont requis'}), 400

        # Créer les joueurs
        print(f"Création des joueurs: {nom_joueur1} et {nom_joueur2}")

        joueur1 = Hero({
            'name': nom_joueur1,
            'profession': 'Guerrier',
            'race': race_humain,
            'classe': classe_guerrier,
            'bag': Bag({'sizeMax': 3, 'items': []}),
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
            'bag': Bag({'sizeMax': 3, 'items': []}),
            'equipment': [],
            'element': 'Eau',
            'life': 100,
            'position': 0
        })

        joueurs=[joueur1,joueur2]

        # Vérification de la création des mobs
        print("Création des mobs...")

        mobs = [
            Mobs({'name': 'Goblin', 'type': 'Goblin', 'race': race_humain, 'classe': classe_guerrier, 
                  'bag': Bag({'sizeMax': 5, 'items': []}), 'equipment': [], 'element': 'Terre', 'life': 5}),
            Mobs({'name': 'Orc', 'type': 'Orc', 'race': race_elfe, 'classe': classe_mage, 
                  'bag': Bag({'sizeMax': 5, 'items': []}), 'equipment': [], 'element': 'Vent', 'life': 15})
        ]

        # Création des items
        items_disponibles = [
            Item({"name": "Épée en fer", "type": "arme", "space": 1}, {"attaque": 10}),
            Item({"name": "Bouclier en bois", "type": "défense", "space": 1}, {"défense": 5}),
            Item({"name": "Potion de soin", "type": "consommable", "space": 1}, {"soin": 20})
        ]

        # Génération des positions
        plateau_size = 50  # Taille du plateau (10 x 5)
        nb_mobs = len(mobs)
        nb_items = len(items_disponibles)

        # Générer des positions uniques pour les mobs et les items
        positions = generer_positions(plateau_size, nb_mobs + nb_items)
        print("Positions générées pour les mobs et items:", positions)

        for j, item in enumerate(items_disponibles):
            item.position = positions[nb_mobs + j]
            print(f"Item {item._name} positionné à {item.position}")

        for i, mob in enumerate(mobs):
            mob.position = positions[ i]
            print(f"Mobs {mob._nom} positionné à {mob.position}")


        return jsonify({
            'message': 'Partie créée avec succès',
            'mobs': [{'name': mob._nom, 'position': mob.position} for mob in mobs],
            'items': [{'name': item._name, 'position': item.position} for item in items_disponibles],
            'joueurs': [joueur.to_dict() for joueur in joueurs]
        })

    except Exception as e:
        print("Une erreur s'est produite:", e)
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
