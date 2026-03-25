# 🌍 iOS GPS Spoofer

Une application bureau moderne et élégante permettant de modifier (spoof) la position GPS de ton iPhone via USB, **sans aucun jailbreak**. 

Développée en Python, elle utilise `pymobiledevice3` pour communiquer avec l'appareil iOS et propose une interface minimaliste (Dark Mode) avec une carte interactive Google Satellite.

## ✨ Fonctionnalités

* **Interface Premium (Dark Mode) :** Design épuré et moderne propulsé par `CustomTkinter`.
* **Carte Interactive en temps réel :** Navigation fluide avec vue hybride (Google Satellite + Noms des rues) via `TkinterMapView`.
* **Sélection au Clic :** Fais un clic-droit n'importe où sur la carte pour définir ta nouvelle position instantanément.
* **Recherche Intelligente :** Tape le nom d'une ville ou d'une adresse pour t'y téléporter.
* **Système de Favoris :** Enregistre tes emplacements préférés (ex: Maison, Bureau) pour y retourner en un clic.
* **Reset Rapide :** Un bouton dédié pour couper le tunnel et rendre à l'iPhone sa position GPS réelle.

## ⚠️ Prérequis INDISPENSABLES

Pour que ton PC puisse communiquer avec ton iPhone, tu dois obligatoirement installer ces deux éléments :

### 1. Python 3 (Via Terminal ou Site)

Tu as besoin de Python sur ton PC. Ouvre ton terminal (cmd) et tape cette commande pour l'installer automatiquement :

```cmd
winget install Python.Python.3.12
```

*(Si tu préfères la méthode classique, télécharge-le sur le [site officiel de Python](https://www.python.org/downloads/). **ATTENTION :** Coche impérativement la case "Add Python to PATH" lors de l'installation !).*

### 2. iTunes (Version site d'Apple ⚠️)

Ton PC a besoin des vrais pilotes USB Apple. 
❌ **NE TÉLÉCHARGE PAS** la version du Microsoft Store (elle ne contient pas les bons pilotes).
✅ **TÉLÉCHARGE** la version classique Windows (64-bit) directement depuis le site d'Apple en cliquant sur ce lien : [Télécharger iTunes pour Windows (Apple.com)](https://www.apple.com/itunes/download/win64).

## 🚀 Comment l'installer et l'utiliser (Méthode Facile)

Pas besoin de savoir coder pour utiliser ce logiciel. Suis ces étapes :

1. **Télécharge le projet :** Rends-toi sur [https://github.com/labetelanimal/ios-gps-spoofer](https://github.com/labetelanimal/ios-gps-spoofer), clique sur le bouton vert **"Code"** en haut de la page, puis sur **"Download ZIP"**. Extrais le dossier sur ton bureau.
2. **Branche ton iPhone :** Connecte ton iPhone en USB à ton PC. Déverrouille ton écran, et si un message apparaît, clique impérativement sur **"Faire confiance à cet ordinateur"** et tape ton code PIN.
3. **Lance le logiciel :** Rends-toi dans le dossier que tu as extrait, et double-clique sur le fichier **`Lancer_GPS_Spoofer.bat`**.
   *(Note : Lors de la première ouverture, une fenêtre noire va s'ouvrir pour télécharger automatiquement les outils nécessaires. Laisse-la faire, ton interface apparaîtra juste après !).*
4. **Alterne tes positions :** Choisis un lieu sur la carte, clique sur **"Appliquer la position"**, et observe ton GPS changer ! Pour arrêter, clique simplement sur **"Reset GPS"**.

## 🛑 Avertissement / Disclaimer

Ce projet est fourni à des fins éducatives et de test uniquement. L'utilisation de ce logiciel pour tricher dans des jeux géolocalisés (ex: Pokémon GO) ou contourner des restrictions de sécurité peut entraîner le bannissement définitif de tes comptes sur ces plateformes. L'auteur n'est pas responsable de l'utilisation qui en est faite.
