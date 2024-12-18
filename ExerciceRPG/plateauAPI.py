import random
from Quest import Quest
from Mobs import Mobs
from flask import Flask, request, jsonify, render_template


app = Flask(__name__)

# Variables globales pour les joueurs, mobs et items

# -----------------------------
# FONCTIONS DE VOTRE CODE
# -----------------------------
def ajouter_item_aleatoire(bag, items_disponibles):
    item = random.choice(items_disponibles)
    if bag.addItem(item):
        return {"status": "success", "message": f"L'item {item._name} a été ajouté au sac du joueur !"}
    else:
        return {"status": "error", "message": "Le sac est plein, impossible d'ajouter un nouvel item."}

def combat(joueur1, joueur2, items_disponibles):
    rounds = []
    round_number = 1

    while joueur1._life > 0 and joueur2._life > 0:
        round_log = {"round": round_number, "actions": []}
        if joueur1.initiative() > joueur2.initiative():
            dommage = joueur1.damages()
            joueur2.defense(dommage)
            round_log["actions"].append(f"{joueur1._nom} attaque {joueur2._nom} pour {dommage} dégâts")

            if joueur2._life <= 0:
                return {"winner": joueur1._nom, "log": rounds + [round_log]}

            dommage = joueur2.damages()
            joueur1.defense(dommage)
            round_log["actions"].append(f"{joueur2._nom} attaque {joueur1._nom} pour {dommage} dégâts")
        else:
            dommage = joueur2.damages()
            joueur1.defense(dommage)
            round_log["actions"].append(f"{joueur2._nom} attaque {joueur1._nom} pour {dommage} dégâts")

            if joueur1._life <= 0:
                return {"winner": joueur2._nom, "log": rounds + [round_log]}

            dommage = joueur1.damages()
            joueur2.defense(dommage)
            round_log["actions"].append(f"{joueur1._nom} attaque {joueur2._nom} pour {dommage} dégâts")

        rounds.append(round_log)
        round_number += 1

    return {"winner": None, "log": rounds}

def combatPVE(joueur, mob, items_disponibles):
    log = []
    while joueur._life > 0 and mob._life > 0:
        dommage = joueur.damages()
        mob.defense(dommage)
        log.append(f"{joueur._nom} attaque {mob._nom} pour {dommage} dégâts")
        
        if mob._life <= 0:
            mob.reset()
            return {"winner": joueur._nom, "log": log}
        
        dommage = mob.damages()
        joueur.defense(dommage)
        log.append(f"{mob._nom} attaque {joueur._nom} pour {dommage} dégâts")

    return {"winner": None, "log": log}

# -----------------------------
# ROUTES DE L'API
# -----------------------------
@app.route('/')
def home():
    return render_template('test.html')


@app.route('/init', methods=['POST'])
def init_game():
    global players, mobs, items_disponibles

    data = request.json
    players = data["players"]
    mobs = [Mobs(**mob_data) for mob_data in data["mobs"]]
    items_disponibles = data["items_disponibles"]
    return jsonify({"status": "success", "message": "Jeu initialisé !"})

@app.route('/combat', methods=['POST'])
def route_combat():
    data = request.json
    joueur1 = players[data['joueur1']]
    joueur2 = players[data['joueur2']]
    result = combat(joueur1, joueur2, items_disponibles)
    return jsonify(result)

@app.route('/combatPVE', methods=['POST'])
def route_combatPVE():
    data = request.json
    joueur = players[data['joueur']]
    mob = next(m for m in mobs if m._nom == data['mob'])
    result = combatPVE(joueur, mob, items_disponibles)
    return jsonify(result)

@app.route('/jouer', methods=['POST'])
def route_jouer():
    data = request.json
    joueur1 = players[data['joueur1']]
    joueur2 = players[data['joueur2']]
    plateau_taille = data.get("plateau_taille", 50)
    log = []

    while joueur1._life > 0 and joueur2._life > 0:
        de1 = random.randint(1, 6)
        joueur1._position += de1
        log.append(f"{joueur1._nom} a avancé de {de1} cases. Position actuelle : {joueur1._position}")

        if random.random() < 0.3:
            mob = random.choice(mobs)
            log.append(f"{joueur1._nom} rencontre un {mob._nom} !")
            log += combatPVE(joueur1, mob, items_disponibles)["log"]

        de2 = random.randint(1, 6)
        joueur2._position += de2
        log.append(f"{joueur2._nom} a avancé de {de2} cases. Position actuelle : {joueur2._position}")

        if random.random() < 0.3:
            mob = random.choice(mobs)
            log.append(f"{joueur2._nom} rencontre un {mob._nom} !")
            log += combatPVE(joueur2, mob, items_disponibles)["log"]

        if joueur1._position == joueur2._position:
            log.append("Combat entre les deux joueurs !")
            result = combat(joueur1, joueur2, items_disponibles)
            log += result["log"]

        if joueur1._position >= plateau_taille:
            return jsonify({"winner": joueur1._nom, "log": log})
        elif joueur2._position >= plateau_taille:
            return jsonify({"winner": joueur2._nom, "log": log})

    return jsonify({"winner": None, "log": log})

# -----------------------------
# LANCEMENT DU SERVEUR
# -----------------------------
if __name__ == '__main__':
    app.run(debug=True)
