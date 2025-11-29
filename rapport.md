\newpage

# 1. Introduction

## 1.1 Contexte et Objectif
Ce rapport synthétise la démarche et les résultats obtenus dans le cadre de "Introduction à l'IA" (2IA). L'objectif principal est de mettre en oeuvre et de comparer les performances de plusieurs algorithmes de recherche sur des problèmes types représentatifs.

Cette étude vise à évaluer les points forts, les limites et les comportements des méthodes de recherche (informées et non informées). L'analyse s'appuie essentiellement sur deux indicateurs clés : le temps de calcul nécessaire pour trouver une solution et l'espace mémoire utilisé. Nous observerons également l'impact de la taille des instances et des stratégies d'initialisation sur ces performances.

## 1.2 Problèmes traités
Conformément aux directives suggérant des problèmes de type "plus court chemin" ou des jeux combinatoires, nous avons choisi d'analyser les performances de nos algorithmes sur trois domaines distincts :

- **Recherche de chemin dans un graphe général :**
    Application des algorithmes de base pour explorer la connectivité et l'optimalité sur des graphes abstraits.
    - *Algorithmes testés :* BFS, DFS, Dijkstra.

- **Navigation sur grille avec obstacles :**
    Recherche de chemin dans un environnement 2D (grille) impliquant une topologie régulière mais contrainte par une densité variable d'obstacles.
    - *Algorithmes testés :* BFS, DFS, Dijkstra, A\*, IDA\*.

- **Les Tours de Hanoï[^1] :**
    Résolution d'un problème combinatoire classique, permettant d'évaluer la capacité des algorithmes à gérer un espace d'états croissant exponentiellement avec le nombre de disques (similaire à la complexité du Taquin).
    - *Algorithmes testés :* DFS, BFS, Dijkstra, A\*, IDA\*.

[^1]: Voir la définition et les règles du problème sur [Wikipedia - Tours de Hanoï](https://fr.wikipedia.org/wiki/Tours_de_Hano%C3%AF).


# 2. Méthodologie

## 2.1 Environnement technique

Conformément aux modalités laissant le choix des technologies libre, nous avons développé nos solutions en utilisant l'environnement suivant :

- **Langage :** Python 3.12.3.
- **Système d'exploitation :** Ubuntu 24.04.3 LTS.
- **Matériel de test :** Les benchmarks ont été exécutés sur un ordinateur portable ASUS Vivobook (M3500QC) équipé de :
    - **Processeur :** AMD Ryzen™ 5 5600H 
    - **Mémoire (RAM) :** 16 Go.

- **Code source :** Les sources des programmes utilisés ainsi que les jeux de données sont fournis en annexe.


