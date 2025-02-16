import random

def choisir_mot():
    mots = ["python", "ordinateur", "programmation", "intelligence", "artificielle"]
    return random.choice(mots)

def afficher_mot(mot, lettres_trouvees):
    affichage = ""
    for lettre in mot:
        if lettre in lettres_trouvees:
            affichage += lettre
        else:
            affichage += "_"
    return affichage

def jouer():
    mot = choisir_mot()
    lettres_trouvees = []
    essais_restants = 6
    print("Bienvenue au jeu du pendu !")

    while essais_restants > 0:
        print("\nMot à deviner : ", afficher_mot(mot, lettres_trouvees))
        lettre = input("Proposez une lettre : ").lower()

        if lettre in lettres_trouvees:
            print("Vous avez déjà proposé cette lettre.")
        elif lettre in mot:
            lettres_trouvees.append(lettre)
            print("Bien joué !")
        else:
            essais_restants -= 1
            print("Raté ! Il vous reste", essais_restants, "essais.")

        if set(mot) == set(lettres_trouvees):
            print("\nFélicitations ! Vous avez deviné le mot :", mot)
            break
    else:
        print("\nDommage ! Le mot était :", mot)

if __name__ == "__main__":
    jouer()
