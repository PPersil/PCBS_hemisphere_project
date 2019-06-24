from random import *
import random
import numpy as np
import expyriment
from  expyriment.stimuli import FixCross, BlankScreen
import matplotlib.pyplot as plt
import statistics as pystat

# Définition des listes pour stocker les temps de réactions
temps_homolateral = []
temps_controlateral=[]


#initiation de l'experience
exp = expyriment.design.Experiment(name="Test de croisement hemisphérique")
expyriment.control.initialize(exp)

# Nombre de test par block
n_trials = 8
# Nombre de bloc d'experience
n_blocks = 4


MAXDURATION = 2000

# Création des stimuli
target_droite = FixCross(size=(500, 500), line_width=80, position=(-500,0))
target_gauche = FixCross(size=(500, 500), line_width=80, position=(500,0))


blankscreen = BlankScreen()
expyriment.control.start(skip_ready_screen = True)

## EXPERIENCE ##

#Affichage des instructions
expyriment.stimuli.TextScreen(
    "Quand la croix apparaitra à droite, appuyez sur le clavier avec votre main droite",
    "Quand la croix apparaitra à gauche, appuyez sur le clavier avec votre main gauche").present()
exp.keyboard.wait() # début l'experience à l'appuie d'une touche
blankscreen.present()

clock = expyriment.misc.Clock()
for j in range(n_blocks): # pour avancer de bloc en bloc
    if (j%2 == 0) :  # blocs ou l'oeil droit est caché
        oeil_cache = "droit"
        expyriment.stimuli.TextScreen(
            "Attrapez un foulard et cachez votre oeil droit",
            "Appuyez sur une touche pour continuer").present()
        exp.keyboard.wait()
        blankscreen.present()
        for i in range(n_trials): # necessaire pour randomiser la position de la croix à chaque fois
            c = randint (1,2) # randomise la position de la croix
            if c == 2: # cas où la croix sera à droite
                cote = "droit"
                waitingtime = 2000 + int(1000 * random.expovariate(3)) # Ajoute une randomisation du temps d'apparition
                exp.clock.wait(waitingtime)
                time = clock.time # Chronometre
                target_droite.present() # Affichage du stimulus
                key, rt = exp.keyboard.wait(duration=MAXDURATION)
                exp.data.add([time, i, waitingtime, key, rt, oeil_cache, cote]) #Creation d'un fichier de données
                temps_homolateral.append(rt) # Creation de la liste de temps de reaction
                blankscreen.present()
            else : # cas où la croix sera à gauche
                cote = "gauche"
                waitingtime = 2000 + int(1000 * random.expovariate(3)) # Ajoute une randomisation du temps d'apparition
                exp.clock.wait(waitingtime)
                time = clock.time # Chronometre
                target_gauche.present() # Affichage du stimulus
                key, rt = exp.keyboard.wait(duration=MAXDURATION)
                exp.data.add([time, i, waitingtime, key, rt, oeil_cache, cote]) #Creation d'un fichier de données
                temps_controlateral.append(rt) # Creation de la liste de temps de reaction
                blankscreen.present()
    else : # blocs ou l'oeil gauche est caché
        oeil_cache = "gauche"
        expyriment.stimuli.TextScreen(
            "Attrapez un foulard et cachez votre oeil gauche",
            "Appuyez sur une touche pour continuer").present()
        exp.keyboard.wait()
        blankscreen.present()
        for i in range(n_trials):
            c = randint (1,2) # randomise la position de la croix
            if c == 2: # cas où la croix sera à droite
                cote = "droit"
                waitingtime = 2000 + int(1000 * random.expovariate(3)) # Ajoute une randomisation du temps d'apparition
                exp.clock.wait(waitingtime)
                time = clock.time # Chronometre
                target_droite.present() # Affichage du stimulus
                key, rt = exp.keyboard.wait(duration=MAXDURATION)
                exp.data.add([time, i, waitingtime, key, rt, oeil_cache, cote]) #Creation d'un fichier de données
                temps_controlateral.append(rt) # Creation de la liste de temps de reaction
                blankscreen.present()
            else : # cas où la croix sera à gauche
                cote = "gauche"
                waitingtime = 2000 + int(1000 * random.expovariate(3)) # Ajoute une randomisation du temps d'apparition
                exp.clock.wait(waitingtime)
                time = clock.time # Chronometre
                target_gauche.present() # Affichage du stimulus
                key, rt = exp.keyboard.wait(duration=MAXDURATION)
                exp.data.add([time, i, waitingtime, key, rt, oeil_cache, cote]) #Creation d'un fichier de données
                temps_homolateral.append(rt) # Creation de la liste de temps de reaction
                blankscreen.present()


expyriment.control.end()

### Graphique en barres
moyenne_TH = pystat.mean(temps_homolateral)
moyenne_TC = pystat.mean(temps_controlateral)
std_TH = np.std(temps_homolateral)
std_TC = np.std(temps_controlateral)

# épaisseur des barres
barWidth = 0.3

# hauteur des barres
bars = [moyenne_TC, moyenne_TH]



# Valeur des barres d'erreurs
yer1 = [std_TC, std_TH]



# Position des barres
r1 = np.arange(len(bars))

# Creation des barres
plt.bar(r1, bars, width = barWidth, color = 'yellow', edgecolor = 'black', yerr=yer1, capsize=7)

# Parametres d'affichaes
plt.xticks(r1, ['Controlateral', 'Homolateral'])
plt.ylabel('Temps de reaction (ms)')
plt.legend()

# Affichage du graphique
plt.show()
