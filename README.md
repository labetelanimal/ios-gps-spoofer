# 🌍 iOS GPS Spoofer

> **Spoof your iPhone's GPS location from Windows — no jailbreak required.**

A modern, open-source desktop app built in Python that lets you simulate any GPS location on your iPhone via USB. Built with `pymobiledevice3` and a clean dark-mode UI featuring a live interactive satellite map.

---

## ✨ Features

- 🗺️ **Live Interactive Map** — Google Satellite + street names via `TkinterMapView`
- 🖱️ **Right-click to place** — Set any location directly on the map in one click
- 🔍 **Smart search** — Search any city, address or landmark worldwide
- ⭐ **Favorites system** — Save your frequent spots (Home, Work, etc.)
- 🌐 **English / French UI** — Switch language from the app
- 📍 **Preset locations** — Paris, Lyon, Geneva, Tokyo, New York and more
- 🔄 **One-click GPS reset** — Instantly restore your real position
- ⚡ **Auto tunnel** — USB tunnel starts automatically, no terminal needed

---

## ⚠️ Requirements

Before using the app, you **must** install these two things:

### 1. Python 3.12+

Open `cmd` and run:
```
winget install Python.Python.3.12
```
> ⚠️ If you install manually from [python.org](https://www.python.org/downloads/), **check "Add Python to PATH"** during installation or nothing will work.

### 2. iTunes (Apple website version — NOT Microsoft Store)

The Microsoft Store version does **not** include the USB drivers needed to communicate with your iPhone.

✅ Download the correct version here: [iTunes for Windows — Apple.com](https://www.apple.com/itunes/download/win64)

---

## 🚀 Installation (Step by Step)

Follow these steps carefully. We went through a lot of trial and error so you don't have to.

### Step 1 — Download the project

Go to [https://github.com/labetelanimal/ios-gps-spoofer](https://github.com/labetelanimal/ios-gps-spoofer), click the green **Code** button → **Download ZIP**, and extract the folder to your Desktop.

### Step 2 — Connect your iPhone

- Plug your iPhone into your PC via USB
- Unlock your screen
- If a popup appears on your iPhone → tap **"Trust This Computer"** and enter your PIN

### Step 3 — Enable Developer Mode on iPhone

Go to: **Settings → Privacy & Security → Developer Mode → Enable**

Your iPhone will restart. Confirm activation after the reboot.

> ⚠️ Developer Mode is **required** on iOS 16 and above. Without it, the GPS simulation service will be blocked.

### Step 4 — Launch the app

Double-click **`Lancer_GPS_Spoofer.bat`**

On first launch, a black window will appear and automatically install all required Python libraries (`pymobiledevice3`, `customtkinter`, `tkintermapview`, etc.). This may take 1–2 minutes. The app will open automatically once done.

> ⚠️ **Run as Administrator** — Right-click `Lancer_GPS_Spoofer.bat` → **Run as administrator**. This is required for the USB tunnel to work on Windows.

### Step 5 — Spoof your location

1. Choose a location on the map (click a preset, search an address, or right-click anywhere on the map)
2. Click **"Apply Location"**
3. The app will automatically:
   - Start the USB tunnel (`lockdown start-tunnel`)
   - Mount the Developer Disk Image
   - Activate GPS simulation
4. Your iPhone's location is now spoofed ✅
5. When done, click **"Reset GPS"** to restore your real position

---

## 🔧 Troubleshooting

We ran into every possible error so here's what actually fixes them:

| Error | Fix |
|---|---|
| `Could not start simulatelocation service` | Enable Developer Mode on iPhone (Settings → Privacy & Security → Developer Mode) |
| `No device found` | Unplug and replug USB, unlock iPhone, tap "Trust This Computer" |
| `Tunnel failed / RSD address not found` | Run the app as Administrator |
| `pymobiledevice3 not found` | Run `python.exe -m pip install pymobiledevice3` in cmd |
| `DeveloperDiskImage timeout` | Wait — it downloads a personalized image from Apple servers, can take 1–2 min |
| App crashes immediately | Make sure Python is added to PATH and you're using Python 3.12+ |
| iTunes error on launch | Rename `iTunes Library.itl` to `iTunes Library.old` in `C:\Users\YOU\Music\iTunes\` |

---

## 📋 How It Works (Technical)

This app uses `pymobiledevice3` to communicate with iOS devices over USB without any jailbreak:

1. **`lockdown start-tunnel`** — Creates an encrypted USB tunnel and returns an RSD (Remote Service Discovery) address
2. **`mounter auto-mount`** — Downloads and mounts a Personalized Developer Disk Image from Apple's servers (required on iOS 17+)
3. **`developer dvt simulate-location set`** — Activates the GPS simulation service via the Developer Tools (DVT) protocol

> 📌 This requires **Developer Mode** to be enabled on the iPhone (iOS 16+). No jailbreak, no Apple account, no Xcode needed.

---

## 📦 Dependencies

All installed automatically by `Lancer_GPS_Spoofer.bat`:

```
pymobiledevice3
customtkinter
tkintermapview
requests
```

---

## 📁 Project Structure

```
ios-gps-spoofer/
├── ios_gps_spoofer.py       # Main application
├── Lancer_GPS_Spoofer.bat   # Windows launcher (auto-installs deps)
├── requirements.txt         # Python dependencies
├── mes_favoris.json         # Your saved favorites (auto-created)
└── README.md
```

---

## 🛑 Disclaimer

This project is provided for **educational and testing purposes only**.  
Using this tool to cheat in location-based games (e.g. Pokémon GO) or bypass security restrictions may result in a **permanent ban** on those platforms. The author is not responsible for any misuse.

---

## 👤 Author

Made by **labetelanimal** — *"I was bored and learning to code, so I built this."*

GitHub: [github.com/labetelanimal](https://github.com/labetelanimal)

---

## ⭐ Support

If this project helped you, leave a ⭐ on GitHub — it means a lot!
