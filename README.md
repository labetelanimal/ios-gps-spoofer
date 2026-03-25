# 🌍 iOS GPS Spoofer

Une application desktop moderne et élégante permettant de modifier (spoof) la position GPS d'un iPhone via USB, **sans aucun jailbreak**. 

Développée en Python, elle utilise `pymobiledevice3` pour communiquer avec l'appareil iOS et propose une interface minimaliste (Dark Mode) avec une carte interactive Google Satellite.

## ✨ Fonctionnalités

* **Interface Premium (Dark Mode) :** Design épuré et moderne propulsé par `CustomTkinter`.
* **Carte Interactive en temps réel :** Navigation fluide avec vue hybride (Google Satellite + Noms des rues) via `TkinterMapView`.
* **Sélection au Clic :** Fais un clic-droit n'importe où sur la carte pour définir ta nouvelle position instantanément.
* **Recherche Intelligente :** Tape le nom d'une ville ou d'une adresse pour t'y téléporter.
* **Système de Favoris :** Enregistre tes emplacements préférés avec un nom personnalisé pour y retourner en un clic.
* **Reset Rapide :** Un bouton dédié pour couper le tunnel et rendre à l'iPhone sa position GPS réelle.

## 🛠️ Prérequis

Avant de lancer le projet, assure-toi d'avoir :
1. **Python 3.x** installé et ajouté au PATH.
2. **iTunes** (ou l'application "Appareils Apple" sur Windows 11) installé pour avoir les pilotes Apple officiels.
3. Un câble USB pour relier l'iPhone au PC (l'iPhone doit avoir "Fait confiance" à l'ordinateur).

## 🚀 Installation

1. Clone ce repository sur ta machine :
   ```bash
   git clone [https://github.com/TON-NOM-UTILISATEUR/ios-gps-spoofer.git](https://github.com/TON-NOM-UTILISATEUR/ios-gps-spoofer.git)
   cd ios-gps-spoofer
