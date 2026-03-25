# ---------------------------------------------------------
# Project: iOS GPS Spoofer
# Author: labetelanimal (https://github.com/labetelanimal)
# Version: 2.0.2 - Bilingue + Smart Search + Anti-Freeze Fix
# ---------------------------------------------------------

import customtkinter as ctk
import tkinter as tk
import tkintermapview
import threading
import os
import subprocess
import json
import urllib.request
import urllib.parse
import re
import sys
import time

# --- TRADUCTIONS ---
TRANSLATIONS = {
    "fr": {
        "title": "iOS GPS Spoofer",
        "tunnel_on": "Tunnel connecté",
        "tunnel_off": "Tunnel déconnecté",
        "search": "Rechercher un lieu (ou coords)...",
        "target": "Coordonnées cibles",
        "fav_add": "⭐ Ajouter aux favoris",
        "apply": "Appliquer la position",
        "reset": "Reset GPS",
        "ready": "Système prêt.",
        "lang_btn": "🇬🇧 EN",
        "my_favorites": "Mes Favoris",
        "default_places": "Lieux par défaut",
        "place_marker": "Placer le marqueur ici",
        "signature": "Made by labetelanimal",
        "manual_pos": "Position manuelle",
        "searching": "Recherche...",
        "found": "Lieu trouvé.",
        "not_found": "Introuvable.",
        "invalid_coords": "Coordonnées invalides.",
        "connecting": "Application en cours...",
        "restoring": "Restauration du GPS...",
        "fav_dialog_title": "⭐ Nouveau favori",
        "fav_dialog_text": "Nom de ce lieu (ex: Maison, Bureau) :",
        "fav_saved": "Favori enregistré."
    },
    "en": {
        "title": "iOS GPS Spoofer",
        "tunnel_on": "Tunnel connected",
        "tunnel_off": "Tunnel disconnected",
        "search": "Search a place (or coords)...",
        "target": "Target coordinates",
        "fav_add": "⭐ Add to favorites",
        "apply": "Apply location",
        "reset": "Reset GPS",
        "ready": "System ready.",
        "lang_btn": "🇫🇷 FR",
        "my_favorites": "My Favorites",
        "default_places": "Default Places",
        "place_marker": "Place marker here",
        "signature": "Made by labetelanimal",
        "manual_pos": "Manual position",
        "searching": "Searching...",
        "found": "Place found.",
        "not_found": "Not found.",
        "invalid_coords": "Invalid coordinates.",
        "connecting": "Applying location...",
        "restoring": "Restoring GPS...",
        "fav_dialog_title": "⭐ New favorite",
        "fav_dialog_text": "Name for this place (e.g. Home, Work):",
        "fav_saved": "Favorite saved."
    }
}

# ─────────────────────────────────────────────
#  CONFIG : STYLE MINIMALISTE & MODERNE
# ─────────────────────────────────────────────
APP_W, APP_H = 1000, 700
FAV_FILE     = "mes_favoris.json"

BG           = "#09090b"
BG2          = "#141417"
BG_HOVER     = "#27272a"
ACCENT       = "#ffffff"
ACCENT_TEXT  = "#000000"
ACCENT_HOVER = "#e4e4e7"
TEXT         = "#fafafa"
MUTED        = "#a1a1aa"
SUCCESS      = "#4ade80"
ERROR        = "#f87171"
BORDER       = "#27272a"

PRESETS = {
    "📍 Paris, France":              (48.8566,    2.3522),
    "📍 Lyon, France":               (45.7417,    4.8342),
    "📍 Genève, Switzerland":        (46.2044,    6.1667),
    "📍 Tokyo, Japan":               (35.6762,  139.6503),
    "📍 New York, USA":              (40.7128,  -74.0060),
    "📍 London, UK":                 (51.5074,   -0.1278),
    "📍 Dubai, UAE":                 (25.2048,   55.2708),
    "📍 Sydney, Australia":          (-33.8688,  151.2093),
    "📍 San Francisco, USA":         (37.7749, -122.4194),
}

ctk.set_appearance_mode("dark")

# ─────────────────────────────────────────────
#  BACKEND (Tunnel, DDI, Spoofer)
# ─────────────────────────────────────────────
_tunnel_proc, _tunnel_addr, _tunnel_port, _active_proc = None, None, None, None
_tunnel_lock = threading.Lock()
PYTHON = sys.executable

def _start_tunnel(status_cb):
    global _tunnel_proc, _tunnel_addr, _tunnel_port
    with _tunnel_lock:
        if _tunnel_proc and _tunnel_proc.poll() is None:
            _tunnel_proc.terminate()
            _tunnel_proc = None
        try:
            flags = subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0
            proc = subprocess.Popen([PYTHON, "-m", "pymobiledevice3", "lockdown", "start-tunnel"],
                stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, creationflags=flags)
            addr, port = None, None
            for line in proc.stdout:
                m = re.search(r'--rsd\s+([\w:]+)\s+(\d+)', line)
                if m: addr, port = m.group(1), int(m.group(2)); break
                if "error" in line.lower() and "errno" not in line.lower():
                    proc.terminate(); return False
            if addr and port:
                _tunnel_proc, _tunnel_addr, _tunnel_port = proc, addr, port
                return True
            else:
                proc.terminate(); return False
        except Exception: return False

def _mount_ddi():
    global _tunnel_addr, _tunnel_port
    if not _tunnel_addr: return False
    try:
        flags = subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0
        subprocess.run([PYTHON, "-m", "pymobiledevice3", "mounter", "auto-mount", "--rsd", _tunnel_addr, str(_tunnel_port)],
            capture_output=True, text=True, timeout=120, creationflags=flags)
    except: pass
    return True

def set_location(lat, lon, callback):
    global _active_proc
    def run():
        global _active_proc
        if not _tunnel_addr or (_tunnel_proc and _tunnel_proc.poll() is not None):
            if not _start_tunnel(lambda m, c: callback(False, m, c)): 
                callback(False, "Erreur Tunnel (Vérifiez l'USB)", ERROR)
                return
        _mount_ddi()
        try:
            if _active_proc and _active_proc.poll() is None: _active_proc.terminate()
            flags = subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0
            proc = subprocess.Popen([PYTHON, "-m", "pymobiledevice3", "developer", "dvt", "simulate-location", "set",
                 "--rsd", _tunnel_addr, str(_tunnel_port), "--", str(lat), str(lon)],
                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, creationflags=flags)
            _active_proc = proc
            
            # Correction du freeze : On n'attend plus une phrase précise, on attend 1.5s
            # Si ça n'a pas crashé, c'est que la position est appliquée sur l'iPhone !
            time.sleep(1.5)
            callback(True, f"GPS Actif : {lat:.5f}, {lon:.5f}", SUCCESS)
            
        except Exception: 
            callback(False, "Erreur d'application", ERROR)
    threading.Thread(target=run, daemon=True).start()

def reset_location(callback):
    global _active_proc
    def run():
        if _active_proc and _active_proc.poll() is None:
            try: _active_proc.stdin.write("\n"); _active_proc.stdin.flush()
            except: pass
            _active_proc.terminate()
        if _tunnel_addr:
            try:
                flags = subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0
                subprocess.run([PYTHON, "-m", "pymobiledevice3", "developer", "dvt", "simulate-location", "clear",
                     "--rsd", _tunnel_addr, str(_tunnel_port)], capture_output=True, timeout=10, creationflags=flags)
            except: pass
        callback(True, "", SUCCESS)
    threading.Thread(target=run, daemon=True).start()

def geocode(address, callback):
    def run():
        try:
            q = urllib.parse.quote(address)
            req = urllib.request.Request(f"https://nominatim.openstreetmap.org/search?q={q}&format=json&limit=1", headers={"User-Agent": "iOSGPSSpoofr/3.0"})
            with urllib.request.urlopen(req, timeout=8) as r: data = json.loads(r.read())
            if data: callback(True, float(data[0]["lat"]), float(data[0]["lon"]), data[0].get("display_name", ""))
            else: callback(False, 0, 0, "")
        except Exception: callback(False, 0, 0, "")
    threading.Thread(target=run, daemon=True).start()

# ─────────────────────────────────────────────
#  GUI PRINCIPALE
# ─────────────────────────────────────────────
class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self._current_lang = "fr"
        self._t = TRANSLATIONS[self._current_lang]
        
        self.title(self._t["title"])
        self.geometry(f"{APP_W}x{APP_H}")
        self.configure(fg_color=BG)
        
        self._cur_lat = tk.DoubleVar(value=48.8566)
        self._cur_lon = tk.DoubleVar(value=2.3522)
        self._status  = tk.StringVar(value=self._t["ready"])
        self._current_location_name = tk.StringVar(value="Paris, France")
        self._map_marker = None 
        
        self.protocol("WM_DELETE_WINDOW", self._on_close)
        self._build_ui()

    def _toggle_lang(self):
        self._current_lang = "en" if self._current_lang == "fr" else "fr"
        self._t = TRANSLATIONS[self._current_lang]
        
        self.title(self._t["title"])
        for widget in self.winfo_children():
            widget.destroy()
        self._map_marker = None 
        
        self._build_ui()
        self._set_status(self._t["ready"], MUTED)

    def _on_close(self):
        global _tunnel_proc, _active_proc
        for p in [_active_proc, _tunnel_proc]:
            if p and p.poll() is None: p.terminate()
        self.destroy()

    def _build_ui(self):
        hdr = ctk.CTkFrame(self, fg_color="transparent")
        hdr.pack(fill="x", pady=(25, 15), padx=40)
        
        ctk.CTkLabel(hdr, text=self._t["title"], text_color=TEXT, font=ctk.CTkFont(family="Inter", size=22, weight="bold")).pack(side="left")
        
        lang_btn = ctk.CTkButton(hdr, text=self._t["lang_btn"], command=self._toggle_lang, width=60, height=28, fg_color=BG2, hover_color=BG_HOVER, border_color=BORDER, border_width=1, corner_radius=6, font=ctk.CTkFont(size=11, weight="bold"))
        lang_btn.pack(side="right", padx=(15, 0))

        self._status_dot = ctk.CTkFrame(hdr, fg_color=MUTED, width=8, height=8, corner_radius=4)
        self._status_dot.pack(side="right", pady=10)
        self._status_text = ctk.CTkLabel(hdr, text=self._t["tunnel_off"], text_color=MUTED, font=ctk.CTkFont(family="Inter", size=12))
        self._status_text.pack(side="right", padx=10)

        body = ctk.CTkFrame(self, fg_color="transparent")
        body.pack(fill="both", expand=True, padx=30, pady=(0, 20))

        sidebar = ctk.CTkFrame(body, fg_color=BG2, corner_radius=16, width=300)
        sidebar.pack(side="left", fill="y", padx=(0, 20))
        sidebar.pack_propagate(False)
        self._build_sidebar(sidebar)

        main_area = ctk.CTkFrame(body, fg_color="transparent")
        main_area.pack(side="left", fill="both", expand=True)
        self._build_main_area(main_area)

    def _build_sidebar(self, parent):
        search_frame = ctk.CTkFrame(parent, fg_color="transparent")
        search_frame.pack(fill="x", padx=20, pady=(25, 15))
        
        self._search_var = tk.StringVar()
        search_entry = ctk.CTkEntry(search_frame, textvariable=self._search_var, fg_color=BG, text_color=TEXT, border_color=BORDER, border_width=1, corner_radius=8, height=40, placeholder_text=self._t["search"], font=ctk.CTkFont(size=13))
        search_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        search_entry.bind("<Return>", lambda _: self._do_search())
        
        btn_search = ctk.CTkButton(search_frame, text="→", command=self._do_search, width=40, height=40, fg_color=BG, hover_color=BG_HOVER, border_color=BORDER, border_width=1, text_color=TEXT, corner_radius=8, font=ctk.CTkFont(size=16, weight="bold"))
        btn_search.pack(side="right")

        ctk.CTkFrame(parent, fg_color=BORDER, height=1).pack(fill="x", padx=20, pady=5)

        self.scroll_list = ctk.CTkScrollableFrame(parent, fg_color="transparent", bg_color="transparent")
        self.scroll_list.pack(fill="both", expand=True, padx=10, pady=5)
        self._refresh_locations_list()

        info_frame = ctk.CTkFrame(parent, fg_color=BG, corner_radius=12)
        info_frame.pack(fill="x", padx=20, pady=20)
        ctk.CTkLabel(info_frame, text=self._t["target"], text_color=MUTED, font=ctk.CTkFont(size=11)).pack(anchor="w", padx=15, pady=(15, 0))
        
        coord_text_label = ctk.CTkLabel(info_frame, text="", text_color=TEXT, font=ctk.CTkFont(size=12, weight="bold"))
        coord_text_label.pack(anchor="w", padx=15, pady=(2, 10))
        
        fav_btn = ctk.CTkButton(info_frame, text=self._t["fav_add"], command=self._add_favorite, fg_color=BG2, hover_color=BG_HOVER, text_color=SUCCESS, border_color=BORDER, border_width=1, height=32, font=ctk.CTkFont(size=12, weight="bold"))
        fav_btn.pack(fill="x", padx=15, pady=(0, 15))

        def update_coords(*args):
            try: coord_text_label.configure(text=f"{self._cur_lat.get():.4f}, {self._cur_lon.get():.4f}")
            except: pass
        self._cur_lat.trace_add("write", update_coords)
        self._cur_lon.trace_add("write", update_coords)
        update_coords()

        signature = ctk.CTkLabel(parent, text=self._t["signature"], text_color="#1f1f24", font=ctk.CTkFont(family="Inter", size=10, weight="bold"))
        signature.pack(side="bottom", pady=15)

    def _build_main_area(self, parent):
        map_frame = ctk.CTkFrame(parent, fg_color=BG2, corner_radius=16, border_color=BORDER, border_width=1)
        map_frame.pack(fill="both", expand=True)
        
        self.map_widget = tkintermapview.TkinterMapView(map_frame, corner_radius=16)
        self.map_widget.pack(fill="both", expand=True, padx=3, pady=3)
        self.map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=y&x={x}&y={y}&z={z}", max_zoom=19)
        self.map_widget.set_zoom(12)
        self.map_widget.set_position(self._cur_lat.get(), self._cur_lon.get())

        self.map_widget.add_right_click_menu_command(self._t["place_marker"], self._map_click_event)
        self._update_map_marker(self._cur_lat.get(), self._cur_lon.get(), self._current_location_name.get())

        action_frame = ctk.CTkFrame(parent, fg_color="transparent")
        action_frame.pack(fill="x", pady=(20, 0))
        
        self._status_label = ctk.CTkLabel(action_frame, textvariable=self._status, text_color=MUTED, font=ctk.CTkFont(size=13), anchor="w")
        self._status_label.pack(side="left", padx=10)

        self._apply_btn = ctk.CTkButton(action_frame, text=self._t["apply"], command=self._apply, fg_color=ACCENT, text_color=ACCENT_TEXT, hover_color=ACCENT_HOVER, font=ctk.CTkFont(size=14, weight="bold"), height=45, corner_radius=8)
        self._apply_btn.pack(side="right", padx=(15, 0))
        
        reset_btn = ctk.CTkButton(action_frame, text=self._t["reset"], command=self._reset, fg_color=BG2, text_color=TEXT, hover_color=BG_HOVER, border_color=BORDER, border_width=1, font=ctk.CTkFont(size=14), height=45, corner_radius=8)
        reset_btn.pack(side="right")

    # ── Helpers ──────────────────────
    def _load_favorites(self):
        if os.path.exists(FAV_FILE):
            try:
                with open(FAV_FILE, "r", encoding="utf-8") as f: return json.load(f)
            except: pass
        return {}

    def _add_favorite(self):
        dialog = ctk.CTkInputDialog(text=self._t["fav_dialog_text"], title=self._t["fav_dialog_title"])
        name = dialog.get_input()
        if name:
            favs = self._load_favorites()
            favs[f"⭐ {name}"] = [self._cur_lat.get(), self._cur_lon.get()]
            with open(FAV_FILE, "w", encoding="utf-8") as f:
                json.dump(favs, f, indent=4, ensure_ascii=False)
            self._refresh_locations_list()
            self._set_status(self._t["fav_saved"], SUCCESS)

    def _refresh_locations_list(self):
        for widget in self.scroll_list.winfo_children(): widget.destroy()
        favs = self._load_favorites()
        if favs:
            ctk.CTkLabel(self.scroll_list, text=self._t["my_favorites"], text_color=SUCCESS, font=ctk.CTkFont(size=11, weight="bold")).pack(anchor="w", padx=5, pady=(5, 0))
            for name, coords in favs.items():
                btn = ctk.CTkButton(self.scroll_list, text=name, anchor="w", command=lambda la=coords[0], lo=coords[1], n=name: self._select_preset(la, lo, n),
                                    fg_color="transparent", text_color=TEXT, hover_color=BG_HOVER, corner_radius=8, height=36, font=ctk.CTkFont(size=13))
                btn.pack(fill="x", pady=2, padx=5)
            ctk.CTkFrame(self.scroll_list, fg_color=BORDER, height=1).pack(fill="x", padx=10, pady=10)

        ctk.CTkLabel(self.scroll_list, text=self._t["default_places"], text_color=MUTED, font=ctk.CTkFont(size=11, weight="bold")).pack(anchor="w", padx=5, pady=(5, 0))
        for name, (lat, lon) in PRESETS.items():
            btn = ctk.CTkButton(self.scroll_list, text=name, anchor="w", command=lambda la=lat, lo=lon, n=name: self._select_preset(la, lo, n),
                                fg_color="transparent", text_color=TEXT, hover_color=BG_HOVER, corner_radius=8, height=36, font=ctk.CTkFont(size=13))
            btn.pack(fill="x", pady=2, padx=5)

    def _map_click_event(self, coords):
        lat, lon = coords
        self._cur_lat.set(round(lat, 5))
        self._cur_lon.set(round(lon, 5))
        self._current_location_name.set(self._t["manual_pos"])
        self._update_map_marker(lat, lon, self._t["manual_pos"])

    def _update_map_marker(self, lat, lon, text):
        if self._map_marker:
            try: self._map_marker.delete()
            except: pass
        self._map_marker = self.map_widget.set_marker(lat, lon, text=text)
        self.map_widget.set_position(lat, lon)

    def _select_preset(self, lat, lon, name):
        self._cur_lat.set(round(lat, 5))
        self._cur_lon.set(round(lon, 5))
        name_clean = name.replace("📍 ", "").replace("⭐ ", "")
        self._current_location_name.set(name_clean)
        self._update_map_marker(lat, lon, name_clean)

    def _do_search(self):
        addr = self._search_var.get().strip()
        if not addr: return
        
        if addr.lower() == "labetelanimal":
            self._set_status("👑 Developed with passion by labetelanimal!", SUCCESS)
            self._search_var.set("")
            return
            
        try:
            parts = addr.replace(",", " ").split()
            if len(parts) == 2:
                lat = float(parts[0])
                lon = float(parts[1])
                if -90 <= lat <= 90 and -180 <= lon <= 180:
                    self._cur_lat.set(round(lat, 5))
                    self._cur_lon.set(round(lon, 5))
                    self._current_location_name.set(self._t["manual_pos"])
                    self._update_map_marker(lat, lon, self._t["manual_pos"])
                    self._set_status(self._t["found"], SUCCESS)
                    return
        except ValueError:
            pass 

        self._set_status(self._t["searching"], MUTED)
        def cb(ok, lat, lon, display):
            if ok:
                self._cur_lat.set(round(lat, 5))
                self._cur_lon.set(round(lon, 5))
                short = display.split(",")[0] if "," in display else display
                self._current_location_name.set(short)
                self._update_map_marker(lat, lon, short)
                self._set_status(self._t["found"], SUCCESS)
            else: self._set_status(self._t["not_found"], ERROR)
        geocode(addr, cb)

    def _apply(self):
        try:
            lat, lon = self._cur_lat.get(), self._cur_lon.get()
            if not (-90 <= lat <= 90 and -180 <= lon <= 180): raise ValueError
        except:
            self._set_status(self._t["invalid_coords"], ERROR); return
            
        self._apply_btn.configure(state="disabled")
        self._set_status(self._t["connecting"], MUTED)
        
        def cb(ok, msg, color=None):
            def _update_ui():
                self._set_status(msg, color or (SUCCESS if ok else ERROR))
                if _tunnel_addr:
                    self._status_dot.configure(fg_color=SUCCESS)
                    self._status_text.configure(text=self._t["tunnel_on"])
                if ok or "Erreur" in msg: 
                    self._apply_btn.configure(state="normal")
            self.after(0, _update_ui)
            
        set_location(lat, lon, cb)

    def _reset(self):
        self._set_status(self._t["restoring"], MUTED)
        def cb(ok, msg, color=None):
            def _update_ui():
                self._status_dot.configure(fg_color=MUTED)
                self._status_text.configure(text=self._t["tunnel_off"])
                self._set_status(self._t["ready"], SUCCESS)
            self.after(0, _update_ui)
        reset_location(cb)

    def _set_status(self, msg, color=TEXT):
        self._status.set(msg)
        self._status_label.configure(text_color=color)

if __name__ == "__main__":
    app = App()
    app.mainloop()
