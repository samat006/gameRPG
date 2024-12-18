import random
from Quest import Quest
from Mobs import Mobs


def ajouter_item_aleatoire(bag, items_disponibles):
    item = random.choice(items_disponibles)
    
    if bag.addItem(item):
        print(f"L'item {item._name} a été ajouté au sac du joueur !")
    else:
        print("Le sac est plein, impossible d'ajouter un nouvel item.")
        print(bag) 
        
        # Proposer l'échange d'un item
        choix = input("Le sac est plein. Voulez-vous échanger un item ? (o/n) : ")
        if choix.lower() == 'o':
            print("Voici les items dans votre sac :")
            for index, current_item in enumerate(bag._lItems):
                print(f"{index + 1}. {current_item._name}")
            
            try:
                # Choisir un item à remplacer
                item_index = int(input(f"Entrez le numéro de l'item à échanger contre {item._name} : ")) - 1
                if 0 <= item_index < len(bag._lItems):
                    old_item = bag._lItems[item_index]
                    bag._lItems[item_index] = item  # Remplacement de l'item
                    print(f"L'item {old_item._name} a été échangé contre {item._name}.")
                else:
                    print("Choix invalide. Aucun échange n'a été effectué.")
            except ValueError:
                print("Entrée invalide. Aucun échange n'a été effectué.")
        else:
            print("Aucun échange effectué. L'item n'a pas été ajouté au sac.")



def combat(joueur1, joueur2, items_disponibles):
    print(f"Combat entre {joueur1._nom} et {joueur2._nom} commence !")
    round = 1

    while joueur1._life > 0 and joueur2._life > 0:
        print(f"# Round {round} #")
        print(f"{joueur1._nom} : {joueur1._life} PV | {joueur2._nom} : {joueur2._life} PV")

        # Déterminer qui attaque en premier
        if joueur1.initiative() > joueur2.initiative():
            joueur2.defense(joueur1.damages())
            if joueur2._life <= 0:
                break
            joueur1.defense(joueur2.damages())
        else:
            joueur1.defense(joueur2.damages())
            if joueur1._life <= 0:
                break
            joueur2.defense(joueur1.damages())

        round += 1

    # Résultats du combat
    if joueur1._life <= 0:
        vainqueur = joueur2._nom
        item_gagne = ajouter_item_aleatoire(joueur2.bag, items_disponibles)
    else:
        vainqueur = joueur1._nom
        item_gagne = ajouter_item_aleatoire(joueur1.bag, items_disponibles)

    message = f"{vainqueur} a gagné le combat !"
    print(message)

    return {
        'message': message,
        'vainqueur': vainqueur,
        'item_gagne': item_gagne
    }

def combatPVE(joueur, mob, items_disponibles):
    logs = []
    while joueur._life > 0 and mob._life > 0:
        # Tour du joueur
        damage = joueur.damages()
        mob.defense(damage)
        logs.append(f"{joueur._nom} attaque {mob._nom} pour {damage} dégâts !")
        
        if mob._life <= 0:
            logs.append(f"{mob._nom} est mort !")
            break

        # Tour du mob
        damage = mob.damages()
        joueur.defense(damage)
        logs.append(f"{mob._nom} attaque {joueur._nom} pour {damage} dégâts !")
        
        if joueur._life <= 0:
            logs.append(f"{joueur._nom} est mort !")
            break

    # Ajouter un item si le joueur gagne
    item_gagne = None
    if mob._life <= 0:
        item_gagne = ajouter_item_aleatoire(joueur.bag, items_disponibles)
        logs.append(f"{joueur._nom} récupère l'item : {item_gagne['name']} !")

    return {
        'logs': logs,
        'vainqueur': joueur._nom if mob._life <= 0 else mob._nom,
        'item_gagne': item_gagne
    }



def jouer(joueur1, joueur2, mobs, items_disponibles):
    plateau_taille = 50 
    joueur1.bag.reset()
    joueur2.bag.reset()

    while joueur1._life > 0 and joueur2._life > 0: 
        # Tour de joueur1
        input(f"{joueur1._nom} appuyez sur Entrée pour lancer le dé...")
        de1 = random.randint(1, 6)  # Simule un lancer de dé
        joueur1._position += de1
        print(f"{joueur1._nom} a lancé un {de1} ! Il est maintenant sur la case {joueur1._position}.")

        # Chance de rencontrer un mob
        if random.random() < 0.3:  # 30% de chance de rencontrer un mob
            mob = random.choice(mobs)
            print(f"{joueur1._nom} a rencontré un {mob} !")
            combatPVE(joueur1, mob, items_disponibles)  

        # Tour de joueur2
        input(f"{joueur2._nom} appuyez sur Entrée pour lancer le dé...")
        de2 = random.randint(1, 6)  # Simule un lancer de dé
        joueur2._position += de2
        print(f"{joueur2._nom} a lancé un {de2} ! Il est maintenant sur la case {joueur2._position}.")

        # Chance de rencontrer un mob
        if random.random() < 0.3:  # 30% de chance de rencontrer un mob
            mob = random.choice(mobs)
            mob.reset()
            print(f"{joueur2._nom} a rencontré un {mob} !")
            combatPVE(joueur2, mob, items_disponibles)  # Passer les items disponibles

       
        if joueur1._position == joueur2._position:
            print(f"{joueur1._nom} et {joueur2._nom} sont sur la même case, un combat commence !")
            combat(joueur1, joueur2, items_disponibles)  # Passer les items disponibles


        if joueur1._position >= plateau_taille:
            print(f"{joueur1._nom} a gagné la partie !")
            break
        elif joueur2._position >= plateau_taille:
            print(f"{joueur2._nom} a gagné la partie !")
            break

    print("La partie est terminée !")



