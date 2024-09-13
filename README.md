# 🎨 Jeu Mastermind

Bienvenue dans le jeu **Mastermind** ! 🧠 Ce jeu classique de code secret est maintenant disponible avec une interface graphique en utilisant la bibliothèque `tkinter` de Python. L'objectif est de deviner un code de couleurs secret généré aléatoirement. Le jeu enregistre vos performances dans une base de données SQLite.

## 🚀 Fonctionnalités

- **🔒 Code de Couleurs Unique :** Le code secret est composé de quatre couleurs uniques choisies parmi une liste de couleurs : Rouge (R), Vert (G), Bleu (B), Jaune (Y), Orange (O), et Violet (P).
- **🖼️ Interface Graphique :** Utilisation de `tkinter` pour une interface conviviale où vous sélectionnez vos couleurs via des menus déroulants.
- **👤 Système de Connexion :** Entrez votre pseudonyme avant de commencer à jouer.
- **💾 Stockage des Données :** Les pseudonymes, adresses IP et nombre de tentatives sont stockés dans une base de données SQLite.
- **📜 Journalisation :** Enregistrement des événements importants comme les tentatives, les sélections de couleurs et les résultats du jeu.

## 📦 Prérequis

- **Python 3.x** : Assurez-vous d'avoir Python 3 installé.
- **Modules Python nécessaires :**
  - `tkinter` (pour l'interface graphique)
  - `sqlite3` (pour la base de données)
  - `requests` (pour récupérer l'adresse IP)

Installez les modules requis en utilisant la commande suivante :
    ```
pip install requests
    ```

## 🎮 Comment Jouer

1. **🗃️ Exécuter le Script de Création de la Base de Données :**
   Avant de jouer, créez la base de données SQLite en exécutant le script `create_db.py` :

2. **🕹️ Démarrer le Jeu :**
Lancez le jeu avec le script `mast.py` :

3. **✍️ Entrer Votre Pseudonyme :**
Au début du jeu, entrez votre pseudonyme dans le champ prévu et cliquez sur **Soumettre**.

4. **🎨 Faire Votre Devine :**
- Sélectionnez les couleurs pour votre devine en utilisant les menus déroulants.
- Cliquez sur **Valider** pour vérifier votre devine.
- Le jeu affichera le nombre de correspondances exactes et de couleurs correctes.
- Continuez jusqu'à deviner le code secret.

5. **🏆 Gagner le Jeu :**
- Lorsque vous trouvez le code correct, un message vous félicitera pour votre victoire et le nombre de tentatives sera enregistré dans la base de données.

## 📂 Structure du Code

### 1. Script de Création de la Base de Données (`create_db.py`)

Ce script configure la base de données SQLite et crée la table `users` pour stocker les informations suivantes :
- `id` : ID auto-incrémenté pour chaque utilisateur.
- `username` : Le pseudonyme du joueur.
- `ip_address` : L'adresse IP du joueur.
- `attempts` : Le nombre de tentatives pour deviner le code secret.

Exécutez ce script une fois avant de jouer.

### 2. Script du Jeu (`mastermind_game.py`)

Ce script gère la logique du jeu, l'interface utilisateur et enregistre les données des joueurs dans la base de données après la fin du jeu.

### 📋 Journalisation

Le jeu génère des journaux pour divers événements :
- Tentatives des utilisateurs
- Sélections de couleurs
- Nombre de tentatives
- Résultats du jeu (victoire/perte)

## 📜 Licence

Ce projet est open source et est sous la [Licence MIT](./LICENSE).
