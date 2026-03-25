# 🌍 iOS GPS Spoofer

A modern and elegant desktop application that allows you to modify (spoof) your iPhone's GPS location via USB, **without any jailbreak**. 

Built with Python, it relies on `pymobiledevice3` to communicate with the iOS device and features a minimalist UI (Dark Mode) alongside an interactive Google Satellite map.

## ✨ Features

* **Premium Interface (Dark Mode):** Clean, sleek, and modern design powered by `CustomTkinter`.
* **Real-time Interactive Map:** Smooth navigation with a hybrid view (Google Satellite + Street names) using `TkinterMapView`.
* **Click-to-Spoof:** Right-click anywhere on the map to instantly set your new location.
* **Smart Search:** Type the name of a city or address to instantly teleport there.
* **Favorites System:** Save your preferred spots with a custom name so you can return to them in a single click.
* **Quick Reset:** A dedicated button to kill the tunnel and restore the iPhone's real GPS location.

## 🛠️ Prerequisites

Before running the project, make sure you have the following:
1. **Python 3.x** installed and added to your system's PATH.
2. **iTunes** (or the "Apple Devices" app on Windows 11) installed to ensure you have the official Apple USB drivers.
3. A USB cable to connect your iPhone to your PC (you must tap "Trust This Computer" on your iPhone).

## 🚀 Installation

1. Clone this repository to your local machine:
   ```bash
   git clone [https://github.com/YOUR-USERNAME/ios-gps-spoofer.git](https://github.com/YOUR-USERNAME/ios-gps-spoofer.git)
   cd ios-gps-spoofer
