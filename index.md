# Projet de cognition – Illusion de supériorité des lettres


Le code source est disponible ici :  
https://github.com/gaspardmalh/Projet-cognition-Gaspard-MALHOMME

## README
PROJET : REPRODUCTION DE L'ILLUSION DE HAUTEUR LEXICALE Fichier : iam_illusion.py

DESCRIPTION Ce script est une adaptation gamifiée de l'article scientifique "The letter height superiority illusion" de New et al. (2016).  L'idée est de tester si la lecture d'un mot connu influence notre perception visuelle basique, spécifiquement sa taille.

LE PRINCIPE SCIENTIFIQUE Les chercheurs ont montré que les mots réels sont perçus comme physiquement plus grands que des pseudo-mots (mots inventés ou inversés), même quand ils font exactement la même taille. Selon le modèle d'activation interactive cité dans l'article, c'est parce que notre cerveau reconnait le mot et envoie un signal retour ("feedback") vers les zones visuelles, ce qui "agrandit" artificiellement la perception des traits.




RESULTATS ATTENDUS (LE BIAIS) D'après les résultats de l'étude (Experience 2), on s'attend à deux types d'erreurs chez le joueur :

Sur les essais où les tailles sont identiques : le joueur devrait désigner le Vrai Mot comme étant le plus grand dans la majorité des cas (91% contre des non-mots, 66% contre des miroirs dans l'étude originale).

Quand le Vrai Mot est physiquement plus petit : le biais est si fort que le joueur a souvent du mal à voir la différence et pense que les tailles sont égales, voire que le mot est plus grand.


ADAPTATIONS PAR RAPPORT A L'ARTICLE Pour que ce soit jouable sur un PC normal, j'ai dû modifier quelques paramètres du protocole strict :

Temps d'affichage : L'article utilise 500ms pour empêcher l'oeil de bouger. C'est trop rapide pour un jeu "grand public", donc j'ai mis 1000ms.

Point de fixation : Comme le temps est plus long, il est impératif de ne pas tricher. Dans l'étude, les mots sont à 0.9 degré d'excentricité. Ici, on force ça avec le point rouge central qu'il faut fixer tout du long. Si on regarde les mots en face, l'illusion disparait.

Stimuli : J'ai repris leurs listes de mots (Table 1/Appendix) et les conditions miroirs/syllabes inversées.


INSTALLATION Il faut juste Python et la librairie pygame, je l'ai fait dans un virtual environment sur mon ordinateur.

pip install pygame-ce

LANCEMENT

python iam_illusion.py




