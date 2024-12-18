class Joueur:
    nom = ""
    code = 0
    nbJoueur = 0
    nbPoints = 0
    listPersonnage = []
    def __init__(self,nom,code):
        self.nom = nom
        self.code = code
        code += 1
        code = ("J"+str(code))


    def ajouter_personnage(self,perso):
        if (perso not in self.listPersonnage):
            self.listPersonnage.append(perso)

    def modifier_points(self,points):
        self.nbPoints += points

    def __str__(self):
        return f"Joueur {self.nom} {self.nbPoints} {self.listPersonnage}"