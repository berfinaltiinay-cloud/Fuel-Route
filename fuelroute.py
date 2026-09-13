import tkinter as tk
from tkinter import ttk
import os
import requests
import math
from dotenv import load_dotenv
from pathlib import Path
env_dosyasi = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=env_dosyasi)


pencere = tk.Tk()
pencere.title("FuelRoute")
pencere.geometry("600x850")
pencere.configure(bg="#F4F7FB")
pencere.resizable(False, False)

stil = ttk.Style()
stil.theme_use("clam")
stil.configure(
    "Modern.TCombobox",
    padding=7,
    font=("Arial", 11)
)

baslik = tk.Label(
    pencere,
    text="FUELROUTE",
    font=("Arial", 28, "bold"),
    bg="#F4F7FB",
    fg="#173B5C"
)
baslik.pack(pady=(14, 0))

alt_baslik = tk.Label(
    pencere,
    text="Akıllı yakıt ve rota asistanın",
    font=("Arial", 11),
    bg="#F4F7FB",
    fg="#60758A"
)
alt_baslik.pack(pady=(4, 10))

konum_karti = tk.Frame(
    pencere,
    bg="#FFFFFF",
    highlightbackground="#DCE6F0",
    highlightthickness=1
)
konum_karti.pack(fill="x", padx=28, pady=(0, 10))


# NEREDEN
nereden_yazisi = tk.Label(
    konum_karti,
    text="NEREDEN?",
    font=("Arial", 10, "bold"),
    bg="#FFFFFF",
    fg="#42627F"
)
nereden_yazisi.pack(anchor="w", padx=16, pady=(14, 2))

nereden = tk.Entry(
    konum_karti,
    width=42,
    font=("Arial", 12),
    relief="solid",
    bd=1
)
nereden.pack(fill="x", padx=16, pady=(0, 8), ipady=6)


# NEREYE
nereye_yazisi = tk.Label(
    konum_karti,
    text="NEREYE?",
    font=("Arial", 10, "bold"),
    bg="#FFFFFF",
    fg="#42627F"
)
nereye_yazisi.pack(anchor="w", padx=16, pady=(5, 2))

nereye = tk.Entry(
    konum_karti,
    width=42,
    font=("Arial", 12),
    relief="solid",
    bd=1
)
nereye.pack(fill="x", padx=16, pady=(0, 14), ipady=6)
# GOOGLE PLACES

api_key = os.getenv("GOOGLE_MAPS_API_KEY")

places_url = "https://places.googleapis.com/v1/places:autocomplete"


def google_konum_ara(metin):

    if len(metin.strip()) < 3:
        return []

    if not api_key:
        print("API anahtarı bulunamadı.")
        return []

    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": api_key,
        "X-Goog-FieldMask": "suggestions.placePrediction.placeId,suggestions.placePrediction.text"
    }

    veri = {
        "input": metin,
        "includedRegionCodes": ["tr"]
    }

    try:
        cevap = requests.post(
            places_url,
            headers=headers,
            json=veri,
            timeout=10
        )
    except requests.RequestException as hata:
        print("Google Places bağlantı hatası:", hata)
        return []

    print("Places API durum kodu:", cevap.status_code)

    if cevap.status_code != 200:
        print("Places API cevabı:", cevap.text[:500])
        return []

    sonuc = cevap.json()
    oneriler = []

    for suggestion in sonuc.get("suggestions", []):

        place_prediction = suggestion.get("placePrediction")

        if place_prediction:

            metin_bilgisi = place_prediction.get("text", {}).get("text")

            if metin_bilgisi:
                oneriler.append(metin_bilgisi)

    return oneriler
# NEREDEN ÖNERİLERİ

nereden_onerileri = tk.Listbox(
    konum_karti,
    width=42,
    height=4,
    font=("Arial", 10),
    relief="solid",
    bd=1
)

nereden_onerileri.pack_forget()


def nereden_ara(event=None):

    nereden_onerileri.delete(0, tk.END)

    metin = nereden.get().strip()

    if len(metin) < 3:
        nereden_onerileri.pack_forget()
        return

    oneriler = google_konum_ara(metin)

    if not oneriler:
        nereden_onerileri.pack_forget()
        return

    for oneri in oneriler:
        nereden_onerileri.insert(tk.END, oneri)

    nereden_onerileri.pack(pady=(0, 5), before=nereye_yazisi)


nereden.bind(
    "<KeyRelease>",
    nereden_ara
)
# NEREDEN ÖNERİSİ SEÇİMİ

def nereden_sec(event=None):

    secim = nereden_onerileri.curselection()

    if not secim:
        return

    secilen_konum = nereden_onerileri.get(secim[0])

    nereden.delete(0, tk.END)
    nereden.insert(0, secilen_konum)

    nereden_onerileri.pack_forget()


nereden_onerileri.bind(
    "<<ListboxSelect>>",
    nereden_sec
)# NEREYE ÖNERİLERİ

nereye_onerileri = tk.Listbox(
    konum_karti,
    width=42,
    height=4,
    font=("Arial", 10),
    relief="solid",
    bd=1
)

nereye_onerileri.pack_forget()


def nereye_ara(event=None):
    print("NEREYE ARAMA ÇALIŞTI:", nereye.get())
    nereye_onerileri.delete(0, tk.END)

    metin = nereye.get().strip()

    if len(metin) < 3:
        nereye_onerileri.pack_forget()
        return

    oneriler = google_konum_ara(metin)

    if not oneriler:
        nereye_onerileri.pack_forget()
        return

    for oneri in oneriler:
        nereye_onerileri.insert(tk.END, oneri)

    nereye_onerileri.pack(pady=(0, 5))

nereye.bind(
    "<KeyRelease>",
    nereye_ara
)
print("NEREDEN BIND ÇALIŞTI")


# NEREYE ÖNERİSİ SEÇİMİ

def nereye_sec(event=None):

    secim = nereye_onerileri.curselection()

    if not secim:
        return

    secilen_konum = nereye_onerileri.get(secim[0])

    nereye.delete(0, tk.END)
    nereye.insert(0, secilen_konum)

    nereye_onerileri.pack_forget()


nereye_onerileri.bind(
    "<<ListboxSelect>>",
    nereye_sec
)


# ARABA MARKASI
arac_karti = tk.LabelFrame(
    pencere,
    text="  ARAÇ BİLGİLERİ  ",
    font=("Arial", 11, "bold"),
    bg="#FFFFFF",
    fg="#173B5C",
    highlightbackground="#DCE6F0",
    highlightthickness=1,
    padx=16,
    pady=8
)
arac_karti.pack(fill="x", padx=28, pady=(0, 10))

marka_yazisi = tk.Label(
    arac_karti,
    text="Aracın markası:",
    font=("Arial", 10, "bold"),
    bg="#FFFFFF",
    fg="#42627F"
)
marka_yazisi.pack(anchor="w", pady=(2, 2))


# MARKA VE MODELLER

modeller = {

    "BMW": [
        "1 Serisi",
        "2 Serisi",
        "3 Serisi",
        "4 Serisi",
        "5 Serisi",
        "6 Serisi",
        "7 Serisi",
        "8 Serisi",
        "X1",
        "X2",
        "X3",
        "X4",
        "X5",
        "X6",
        "X7"
    ],

    "Mercedes-Benz": [
        "A Serisi",
        "B Serisi",
        "C Serisi",
        "E Serisi",
        "S Serisi",
        "CLA",
        "GLA",
        "GLB",
        "GLC",
        "GLE",
        "GLS"
    ],

    "Toyota": [
        "Yaris",
        "Corolla",
        "Camry",
        "Auris",
        "Avensis",
        "C-HR",
        "RAV4",
        "Prius",
        "Hilux",
        "Land Cruiser"
    ],

    "Volkswagen": [
        "Polo",
        "Golf",
        "Passat",
        "Jetta",
        "T-Roc",
        "Tiguan",
        "Touareg"
    ],

    "Ford": [
        "Fiesta",
        "Focus",
        "Mondeo",
        "Puma",
        "Kuga",
        "Mustang"
    ],

    "Honda": [
        "Civic",
        "Jazz",
        "Accord",
        "HR-V",
        "CR-V"
    ],

    "Nissan": [
        "Micra",
        "Juke",
        "Qashqai",
        "X-Trail",
        "Navara"
    ],

    "Hyundai": [
        "i10",
        "i20",
        "i30",
        "Elantra",
        "Kona",
        "Tucson",
        "Santa Fe"
    ],

    "Kia": [
        "Picanto",
        "Rio",
        "Ceed",
        "Sportage",
        "Niro",
        "Sorento"
    ],

    "Renault": [
        "Clio",
        "Megane",
        "Symbol",
        "Captur",
        "Austral",
        "Kadjar"
    ],

    "Peugeot": [
        "208",
        "308",
        "408",
        "2008",
        "3008",
        "5008"
    ],

    "Fiat": [
        "500",
        "Panda",
        "Egea",
        "Tipo",
        "Doblo"
    ],

    "Opel": [
        "Corsa",
        "Astra",
        "Insignia",
        "Mokka",
        "Grandland"
    ],

    "Mazda": [
        "Mazda2",
        "Mazda3",
        "Mazda6",
        "CX-3",
        "CX-30",
        "CX-5"
    ],

    "Audi": [
        "A1",
        "A3",
        "A4",
        "A5",
        "A6",
        "A7",
        "A8",
        "Q2",
        "Q3",
        "Q5",
        "Q7",
        "Q8"
    ],

    "Chery": [
        "Tiggo 4",
        "Tiggo 7",
        "Tiggo 8"
    ],

    "Cupra": [
        "Formentor",
        "Leon",
        "Ateca"
    ],

    "Jeep": [
        "Renegade",
        "Compass",
        "Cherokee",
        "Grand Cherokee"
    ],

    "Lexus": [
        "LBX",
        "UX",
        "NX",
        "RX",
        "ES"
    ],

    "MG": [
        "MG3",
        "ZS",
        "HS",
        "MG4"
    ],

    "Mini": [
        "Cooper",
        "Countryman",
        "Clubman"
    ],

    "Seat": [
        "Ibiza",
        "Leon",
        "Arona",
        "Ateca"
    ],

    "Skoda": [
        "Fabia",
        "Scala",
        "Octavia",
        "Superb",
        "Karoq",
        "Kodiaq"
    ],

    "Volvo": [
        "EX30",
        "XC40",
        "XC60",
        "XC90",
        "S60"
    ]
}

ortalama_tuketimler = {
    "BMW": {
        "1 Serisi": {"Benzin": 7.0, "Dizel": 5.2}, "2 Serisi": {"Benzin": 7.3, "Dizel": 5.4},
        "3 Serisi": {"Benzin": 7.2, "Dizel": 5.5, "Hibrit": 5.8}, "4 Serisi": {"Benzin": 7.5, "Dizel": 5.7},
        "5 Serisi": {"Benzin": 8.0, "Dizel": 6.0, "Hibrit": 6.2}, "6 Serisi": {"Benzin": 9.0, "Dizel": 6.8},
        "7 Serisi": {"Benzin": 9.5, "Dizel": 7.0, "Hibrit": 6.8}, "8 Serisi": {"Benzin": 10.0, "Dizel": 7.2},
        "X1": {"Benzin": 7.5, "Dizel": 5.8, "Hibrit": 6.2}, "X2": {"Benzin": 7.7, "Dizel": 6.0},
        "X3": {"Benzin": 8.2, "Dizel": 6.4, "Hibrit": 6.8}, "X4": {"Benzin": 8.5, "Dizel": 6.6},
        "X5": {"Benzin": 9.5, "Dizel": 7.2, "Hibrit": 7.0}, "X6": {"Benzin": 10.0, "Dizel": 7.5},
        "X7": {"Benzin": 11.0, "Dizel": 8.0}
    },
    "Mercedes-Benz": {
        "A Serisi": {"Benzin": 7.0, "Dizel": 5.0, "Hibrit": 5.8}, "B Serisi": {"Benzin": 7.2, "Dizel": 5.2, "Hibrit": 5.9},
        "C Serisi": {"Benzin": 7.5, "Dizel": 5.5, "Hibrit": 6.0}, "E Serisi": {"Benzin": 8.0, "Dizel": 6.0, "Hibrit": 6.3},
        "S Serisi": {"Benzin": 10.0, "Dizel": 7.0, "Hibrit": 7.2}, "CLA": {"Benzin": 7.2, "Dizel": 5.3, "Hibrit": 5.9},
        "GLA": {"Benzin": 7.5, "Dizel": 5.8, "Hibrit": 6.2}, "GLB": {"Benzin": 8.0, "Dizel": 6.2},
        "GLC": {"Benzin": 8.5, "Dizel": 6.5, "Hibrit": 6.8}, "GLE": {"Benzin": 10.0, "Dizel": 7.5, "Hibrit": 7.2},
        "GLS": {"Benzin": 11.5, "Dizel": 8.2}
    },
    "Toyota": {
        "Yaris": {"Benzin": 5.8, "Hibrit": 4.2}, "Corolla": {"Benzin": 7.0, "Dizel": 5.5, "Hibrit": 4.8},
        "Camry": {"Benzin": 8.5, "Hibrit": 5.5}, "Auris": {"Benzin": 6.8, "Dizel": 5.2, "Hibrit": 4.7},
        "Avensis": {"Benzin": 7.5, "Dizel": 5.8}, "C-HR": {"Benzin": 7.2, "Hibrit": 5.0},
        "RAV4": {"Benzin": 8.0, "Dizel": 6.5, "Hibrit": 5.8}, "Prius": {"Hibrit": 4.3},
        "Hilux": {"Dizel": 8.5}, "Land Cruiser": {"Dizel": 10.0}
    },
    "Volkswagen": {
        "Polo": {"Benzin": 6.0, "Dizel": 4.7}, "Golf": {"Benzin": 6.8, "Dizel": 5.0, "Hibrit": 5.4},
        "Passat": {"Benzin": 7.2, "Dizel": 5.4, "Hibrit": 5.8}, "Jetta": {"Benzin": 7.3, "Dizel": 5.5},
        "T-Roc": {"Benzin": 7.2, "Dizel": 5.5}, "Tiguan": {"Benzin": 8.0, "Dizel": 6.0, "Hibrit": 6.3},
        "Touareg": {"Benzin": 10.0, "Dizel": 7.5, "Hibrit": 7.0}
    },
    "Ford": {
        "Fiesta": {"Benzin": 6.2, "Dizel": 4.8}, "Focus": {"Benzin": 7.0, "Dizel": 5.2, "Hibrit": 5.7},
        "Mondeo": {"Benzin": 8.0, "Dizel": 5.8, "Hibrit": 5.5}, "Puma": {"Benzin": 6.8, "Hibrit": 5.6},
        "Kuga": {"Benzin": 8.0, "Dizel": 6.2, "Hibrit": 6.0}, "Mustang": {"Benzin": 11.0}
    },
    "Honda": {
        "Civic": {"Benzin": 7.0, "Dizel": 5.3, "Hibrit": 5.0}, "Jazz": {"Benzin": 6.0, "Hibrit": 4.7},
        "Accord": {"Benzin": 8.0, "Hibrit": 5.5}, "HR-V": {"Benzin": 7.2, "Hibrit": 5.2},
        "CR-V": {"Benzin": 8.5, "Dizel": 6.5, "Hibrit": 6.0}
    },
    "Nissan": {
        "Micra": {"Benzin": 6.0, "Dizel": 4.8}, "Juke": {"Benzin": 7.0, "Dizel": 5.5, "Hibrit": 5.3},
        "Qashqai": {"Benzin": 7.5, "Dizel": 5.8, "Hibrit": 6.0}, "X-Trail": {"Benzin": 8.2, "Dizel": 6.5, "Hibrit": 6.5},
        "Navara": {"Dizel": 8.5}
    },
    "Hyundai": {
        "i10": {"Benzin": 6.0}, "i20": {"Benzin": 6.5, "Dizel": 5.0}, "i30": {"Benzin": 7.0, "Dizel": 5.3, "Hibrit": 5.8},
        "Elantra": {"Benzin": 7.2, "Hibrit": 5.0}, "Kona": {"Benzin": 7.2, "Hibrit": 5.2, "Elektrik": 15.5},
        "Tucson": {"Benzin": 8.2, "Dizel": 6.3, "Hibrit": 6.2}, "Santa Fe": {"Benzin": 9.0, "Dizel": 7.0, "Hibrit": 6.8}
    },
    "Kia": {
        "Picanto": {"Benzin": 6.0}, "Rio": {"Benzin": 6.4, "Dizel": 5.0}, "Ceed": {"Benzin": 7.0, "Dizel": 5.3, "Hibrit": 5.8},
        "Sportage": {"Benzin": 8.0, "Dizel": 6.2, "Hibrit": 6.0}, "Niro": {"Hibrit": 4.8, "Elektrik": 16.0},
        "Sorento": {"Benzin": 9.0, "Dizel": 7.0, "Hibrit": 6.8}
    },
    "Renault": {
        "Clio": {"Benzin": 6.0, "Dizel": 4.5, "Hibrit": 4.5}, "Megane": {"Benzin": 7.0, "Dizel": 5.0, "Hibrit": 5.5, "Elektrik": 16.0},
        "Symbol": {"Benzin": 7.2, "Dizel": 5.2}, "Captur": {"Benzin": 7.0, "Dizel": 5.2, "Hibrit": 5.2},
        "Austral": {"Benzin": 7.2, "Hibrit": 5.5}, "Kadjar": {"Benzin": 7.5, "Dizel": 5.8}
    },
    "Peugeot": {
        "208": {"Benzin": 6.0, "Dizel": 4.6, "Elektrik": 15.5}, "308": {"Benzin": 6.8, "Dizel": 5.0, "Hibrit": 5.4, "Elektrik": 16.0},
        "408": {"Benzin": 7.2, "Hibrit": 5.7}, "2008": {"Benzin": 6.8, "Dizel": 5.0, "Elektrik": 16.0},
        "3008": {"Benzin": 7.5, "Dizel": 5.5, "Hibrit": 6.0}, "5008": {"Benzin": 8.0, "Dizel": 6.0, "Hibrit": 6.3}
    },
    "Fiat": {
        "500": {"Benzin": 6.0, "Hibrit": 5.0, "Elektrik": 14.0}, "Panda": {"Benzin": 6.2, "Hibrit": 5.2},
        "Egea": {"Benzin": 7.0, "Dizel": 5.0}, "Tipo": {"Benzin": 7.0, "Dizel": 5.2}, "Doblo": {"Benzin": 8.0, "Dizel": 6.0}
    },
    "Opel": {
        "Corsa": {"Benzin": 6.2, "Dizel": 4.8, "Elektrik": 16.0}, "Astra": {"Benzin": 7.0, "Dizel": 5.2, "Hibrit": 5.6, "Elektrik": 16.5},
        "Insignia": {"Benzin": 8.0, "Dizel": 6.0}, "Mokka": {"Benzin": 7.0, "Dizel": 5.3, "Elektrik": 16.0},
        "Grandland": {"Benzin": 7.8, "Dizel": 5.8, "Hibrit": 6.0, "Elektrik": 18.0}
    },
    "Mazda": {
        "Mazda2": {"Benzin": 6.0, "Hibrit": 4.5}, "Mazda3": {"Benzin": 7.0, "Dizel": 5.0}, "Mazda6": {"Benzin": 7.8, "Dizel": 5.5},
        "CX-3": {"Benzin": 7.2, "Dizel": 5.5}, "CX-30": {"Benzin": 7.5}, "CX-5": {"Benzin": 8.2, "Dizel": 6.0}
    },
    "Audi": {
        "A1": {"Benzin": 6.2, "Dizel": 4.8}, "A3": {"Benzin": 6.8, "Dizel": 5.0, "Hibrit": 5.5}, "A4": {"Benzin": 7.2, "Dizel": 5.3, "Hibrit": 5.8},
        "A5": {"Benzin": 7.5, "Dizel": 5.5, "Hibrit": 6.0}, "A6": {"Benzin": 8.0, "Dizel": 6.0, "Hibrit": 6.3}, "A7": {"Benzin": 8.5, "Dizel": 6.3, "Hibrit": 6.5},
        "A8": {"Benzin": 9.5, "Dizel": 7.0, "Hibrit": 6.8}, "Q2": {"Benzin": 7.0, "Dizel": 5.3}, "Q3": {"Benzin": 7.5, "Dizel": 5.8, "Hibrit": 6.0},
        "Q5": {"Benzin": 8.5, "Dizel": 6.5, "Hibrit": 6.8}, "Q7": {"Benzin": 10.0, "Dizel": 7.5, "Hibrit": 7.0}, "Q8": {"Benzin": 10.5, "Dizel": 7.8, "Hibrit": 7.2}
    },
    "Chery": {"Tiggo 4": {"Benzin": 8.0}, "Tiggo 7": {"Benzin": 8.5}, "Tiggo 8": {"Benzin": 9.0}},
    "Cupra": {"Formentor": {"Benzin": 8.0, "Hibrit": 6.0}, "Leon": {"Benzin": 7.2, "Dizel": 5.3, "Hibrit": 5.6}, "Ateca": {"Benzin": 8.2, "Dizel": 6.0}},
    "Jeep": {"Renegade": {"Benzin": 8.0, "Dizel": 6.0, "Hibrit": 6.2}, "Compass": {"Benzin": 8.5, "Dizel": 6.3, "Hibrit": 6.5}, "Cherokee": {"Benzin": 10.0, "Dizel": 7.5}, "Grand Cherokee": {"Benzin": 12.0, "Dizel": 8.5, "Hibrit": 8.0}},
    "Lexus": {"LBX": {"Hibrit": 4.8}, "UX": {"Benzin": 7.0, "Hibrit": 5.2, "Elektrik": 17.0}, "NX": {"Benzin": 8.0, "Hibrit": 5.8}, "RX": {"Benzin": 9.0, "Hibrit": 6.5}, "ES": {"Benzin": 8.0, "Hibrit": 5.5}},
    "MG": {"MG3": {"Benzin": 6.5, "Hibrit": 4.8}, "ZS": {"Benzin": 7.5, "Elektrik": 17.0}, "HS": {"Benzin": 8.2, "Hibrit": 6.5}, "MG4": {"Elektrik": 16.0}},
    "Mini": {"Cooper": {"Benzin": 7.0, "Elektrik": 15.0}, "Countryman": {"Benzin": 8.0, "Dizel": 6.0, "Hibrit": 6.2, "Elektrik": 18.0}, "Clubman": {"Benzin": 7.5, "Dizel": 5.5}},
    "Seat": {"Ibiza": {"Benzin": 6.2, "Dizel": 4.8}, "Leon": {"Benzin": 6.8, "Dizel": 5.0, "Hibrit": 5.5}, "Arona": {"Benzin": 6.8, "Dizel": 5.2}, "Ateca": {"Benzin": 7.8, "Dizel": 5.8}},
    "Skoda": {"Fabia": {"Benzin": 6.0, "Dizel": 4.7}, "Scala": {"Benzin": 6.5, "Dizel": 5.0}, "Octavia": {"Benzin": 7.0, "Dizel": 5.2, "Hibrit": 5.6}, "Superb": {"Benzin": 7.5, "Dizel": 5.5, "Hibrit": 5.8}, "Karoq": {"Benzin": 7.5, "Dizel": 5.8}, "Kodiaq": {"Benzin": 8.0, "Dizel": 6.2, "Hibrit": 6.5}},
    "Volvo": {"EX30": {"Elektrik": 17.0}, "XC40": {"Benzin": 8.2, "Dizel": 6.2, "Hibrit": 6.0, "Elektrik": 18.0}, "XC60": {"Benzin": 9.0, "Dizel": 6.8, "Hibrit": 6.5}, "XC90": {"Benzin": 10.0, "Dizel": 7.5, "Hibrit": 7.0}, "S60": {"Benzin": 8.0, "Dizel": 5.8, "Hibrit": 6.0}}
}

versiyonlar = {
    "BMW": {
        "1 Serisi": ["116i", "118i", "120i", "120d"], "2 Serisi": ["218i", "220i", "220d", "230i"],
        "3 Serisi": ["318i", "320i", "320d", "330i", "330e", "340i"], "4 Serisi": ["420i", "420d", "430i", "440i"],
        "5 Serisi": ["520i", "520d", "530i", "530d", "530e", "540i"], "6 Serisi": ["630i", "630d", "640i"],
        "7 Serisi": ["730i", "730d", "740i", "740d", "750i"], "8 Serisi": ["840i", "840d", "850i"],
        "X1": ["sDrive18i", "sDrive20i", "xDrive20d"], "X2": ["sDrive18i", "sDrive20i", "xDrive20d"],
        "X3": ["xDrive20i", "xDrive20d", "xDrive30i", "xDrive30d"], "X4": ["xDrive20i", "xDrive20d", "xDrive30i"],
        "X5": ["xDrive30d", "xDrive40i", "xDrive50e"], "X6": ["xDrive30d", "xDrive40i", "M50i"],
        "X7": ["xDrive30d", "xDrive40i", "M60i"]
    },
    "Mercedes-Benz": {
        "A Serisi": ["A180", "A200", "A220", "A250"], "B Serisi": ["B180", "B200", "B220d"],
        "C Serisi": ["C180", "C200", "C220d", "C300"], "E Serisi": ["E200", "E220d", "E250", "E300", "E350", "E400"],
        "S Serisi": ["S350", "S400", "S450", "S500"], "CLA": ["CLA180", "CLA200", "CLA220d", "CLA250"],
        "GLA": ["GLA180", "GLA200", "GLA220d", "GLA250"], "GLB": ["GLB180", "GLB200", "GLB220d", "GLB250"],
        "GLC": ["GLC200", "GLC220d", "GLC300", "GLC400"], "GLE": ["GLE300d", "GLE350", "GLE400", "GLE450"],
        "GLS": ["GLS350d", "GLS400", "GLS450", "GLS500"]
    },
    "Toyota": {
        "Yaris": ["1.0", "1.3", "1.5", "1.5 Hybrid"], "Corolla": ["1.5", "1.6", "1.8 Hybrid", "2.0 Hybrid"],
        "Camry": ["2.5", "2.5 Hybrid"], "Auris": ["1.33", "1.6", "1.8 Hybrid"], "Avensis": ["1.6", "1.8", "2.0 D-4D"],
        "C-HR": ["1.2 Turbo", "1.8 Hybrid", "2.0 Hybrid"], "RAV4": ["2.0", "2.5 Hybrid"],
        "Prius": ["1.8 Hybrid", "2.0 Hybrid"], "Hilux": ["2.4 D-4D", "2.8 D-4D"],
        "Land Cruiser": ["2.8 D-4D", "3.0 D-4D", "4.5 D-4D"]
    },
    "Volkswagen": {
        "Polo": ["1.0 MPI", "1.0 TSI", "1.0 TDI"], "Golf": ["1.0 TSI", "1.5 TSI", "1.6 TDI", "2.0 TDI", "eHybrid"],
        "Passat": ["1.4 TSI", "1.5 TSI", "2.0 TDI", "GTE"], "Jetta": ["1.2 TSI", "1.4 TSI", "1.6 TDI"],
        "T-Roc": ["1.0 TSI", "1.5 TSI", "2.0 TDI"], "Tiguan": ["1.5 TSI", "2.0 TDI", "eHybrid"],
        "Touareg": ["3.0 TDI", "3.0 TFSI", "eHybrid"]
    },
    "Ford": {
        "Fiesta": ["1.1 Ti-VCT", "1.0 EcoBoost", "1.5 TDCi"], "Focus": ["1.0 EcoBoost", "1.5 EcoBoost", "1.5 EcoBlue"],
        "Mondeo": ["1.5 EcoBoost", "2.0 TDCi", "2.0 Hybrid"], "Puma": ["1.0 EcoBoost", "1.0 EcoBoost Hybrid"],
        "Kuga": ["1.5 EcoBoost", "2.0 EcoBlue", "2.5 Hybrid"], "Mustang": ["2.3 EcoBoost", "5.0 V8"]
    },
    "Honda": {
        "Civic": ["1.5 VTEC Turbo", "1.6 i-DTEC", "2.0 e:HEV"], "Jazz": ["1.3 i-VTEC", "1.5 e:HEV"],
        "Accord": ["2.0", "2.4", "2.0 Hybrid"], "HR-V": ["1.5 i-VTEC", "1.5 e:HEV"],
        "CR-V": ["1.5 VTEC Turbo", "1.6 i-DTEC", "2.0 e:HEV"]
    },
    "Nissan": {
        "Micra": ["1.0 IG-T", "1.2", "1.5 dCi"], "Juke": ["1.0 DIG-T", "1.6 Hybrid", "1.5 dCi"],
        "Qashqai": ["1.3 DIG-T", "1.5 dCi", "e-Power"], "X-Trail": ["1.3 DIG-T", "1.6 dCi", "e-Power"],
        "Navara": ["2.3 dCi 160", "2.3 dCi 190"]
    },
    "Hyundai": {
        "i10": ["1.0 MPI", "1.2 MPI"], "i20": ["1.2 MPI", "1.0 T-GDI", "1.4 CRDi"],
        "i30": ["1.0 T-GDI", "1.5 T-GDI", "1.6 CRDi"], "Elantra": ["1.6 MPI", "1.6 Hybrid"],
        "Kona": ["1.0 T-GDI", "1.6 Hybrid", "Electric 64 kWh"], "Tucson": ["1.6 T-GDI", "1.6 CRDi", "1.6 Hybrid"],
        "Santa Fe": ["1.6 T-GDI Hybrid", "2.2 CRDi", "1.6 Plug-in Hybrid"]
    },
    "Kia": {
        "Picanto": ["1.0 MPI", "1.2 MPI"], "Rio": ["1.2 MPI", "1.0 T-GDI", "1.4 CRDi"],
        "Ceed": ["1.0 T-GDI", "1.5 T-GDI", "1.6 CRDi"], "Sportage": ["1.6 T-GDI", "1.6 CRDi", "1.6 Hybrid"],
        "Niro": ["1.6 Hybrid", "1.6 Plug-in Hybrid", "e-Niro"], "Sorento": ["2.2 CRDi", "1.6 Hybrid", "1.6 Plug-in Hybrid"]
    },
    "Renault": {
        "Clio": ["1.0 TCe", "1.3 TCe", "1.5 dCi", "E-Tech Hybrid"], "Megane": ["1.3 TCe", "1.5 dCi", "E-Tech Electric"],
        "Symbol": ["1.2", "1.5 dCi"], "Captur": ["1.0 TCe", "1.3 TCe", "E-Tech Hybrid"],
        "Austral": ["1.2 E-Tech Hybrid", "1.3 Mild Hybrid"], "Kadjar": ["1.3 TCe", "1.5 dCi", "1.7 Blue dCi"]
    },
    "Peugeot": {
        "208": ["1.2 PureTech", "1.5 BlueHDi", "e-208"], "308": ["1.2 PureTech", "1.5 BlueHDi", "Hybrid 180"],
        "408": ["1.2 PureTech", "Hybrid 180", "Hybrid 225"], "2008": ["1.2 PureTech", "1.5 BlueHDi", "e-2008"],
        "3008": ["1.2 PureTech", "1.5 BlueHDi", "Hybrid 225"], "5008": ["1.2 PureTech", "1.5 BlueHDi", "Hybrid 136"]
    },
    "Fiat": {
        "500": ["1.0 Hybrid", "1.2", "500e"], "Panda": ["1.0 Hybrid", "1.2", "0.9 TwinAir"],
        "Egea": ["1.4 Fire", "1.6 E-Torq", "1.3 Multijet", "1.6 Multijet"], "Tipo": ["1.0 FireFly", "1.4 Fire", "1.6 Multijet"],
        "Doblo": ["1.4 Fire", "1.3 Multijet", "1.6 Multijet"]
    },
    "Opel": {
        "Corsa": ["1.2", "1.2 Turbo", "1.5 Diesel", "Corsa-e"], "Astra": ["1.2 Turbo", "1.5 Diesel", "Plug-in Hybrid"],
        "Insignia": ["1.5 Turbo", "2.0 Turbo", "2.0 Diesel"], "Mokka": ["1.2 Turbo", "1.5 Diesel", "Mokka-e"],
        "Grandland": ["1.2 Turbo", "1.5 Diesel", "Plug-in Hybrid"]
    },
    "Mazda": {
        "Mazda2": ["1.5 Skyactiv-G", "1.5 Hybrid"], "Mazda3": ["1.5 Skyactiv-G", "2.0 Skyactiv-G", "1.8 Skyactiv-D"],
        "Mazda6": ["2.0 Skyactiv-G", "2.5 Skyactiv-G", "2.2 Skyactiv-D"], "CX-3": ["2.0 Skyactiv-G", "1.5 Skyactiv-D"],
        "CX-30": ["2.0 Skyactiv-G", "2.0 Skyactiv-X"], "CX-5": ["2.0 Skyactiv-G", "2.5 Skyactiv-G", "2.2 Skyactiv-D"]
    },
    "Audi": {
        "A1": ["25 TFSI", "30 TFSI", "35 TFSI"], "A3": ["30 TFSI", "35 TFSI", "35 TDI", "40 TFSI"],
        "A4": ["35 TFSI", "40 TFSI", "40 TDI", "45 TFSI"], "A5": ["35 TFSI", "40 TFSI", "40 TDI", "45 TFSI"],
        "A6": ["40 TDI", "45 TFSI", "50 TDI", "55 TFSI"], "A7": ["40 TDI", "45 TDI", "55 TFSI"],
        "A8": ["50 TDI", "55 TFSI", "60 TFSI e"], "Q2": ["30 TFSI", "35 TFSI", "35 TDI"],
        "Q3": ["35 TFSI", "40 TFSI", "40 TDI"], "Q5": ["40 TDI", "45 TFSI", "50 TDI"],
        "Q7": ["45 TDI", "50 TDI", "55 TFSI"], "Q8": ["45 TDI", "50 TDI", "55 TFSI"]
    },
    "Chery": {
        "Tiggo 4": ["1.5 Comfort", "1.5 Pro", "1.5 Turbo"], "Tiggo 7": ["1.5 Comfort", "1.6 TGDI", "1.6 Excellent"],
        "Tiggo 8": ["1.6 TGDI", "2.0 TGDI", "Pro Max"]
    },
    "Cupra": {
        "Formentor": ["1.5 TSI", "2.0 TSI", "e-Hybrid"], "Leon": ["1.5 TSI", "2.0 TSI", "e-Hybrid"],
        "Ateca": ["1.5 TSI", "2.0 TSI", "2.0 TDI"]
    },
    "Jeep": {
        "Renegade": ["1.3 Turbo", "1.6 Multijet", "4xe"], "Compass": ["1.3 Turbo", "1.6 Multijet", "4xe"],
        "Cherokee": ["2.0 Turbo", "2.2 Multijet", "3.2 V6"], "Grand Cherokee": ["2.0 4xe", "3.6 V6", "3.0 CRD"]
    },
    "Lexus": {
        "LBX": ["Elegant", "Relax", "Cool"], "UX": ["UX 200", "UX 250h", "UX 300e"],
        "NX": ["NX 250", "NX 350h", "NX 450h+"], "RX": ["RX 350", "RX 350h", "RX 450h+"],
        "ES": ["ES 200", "ES 300h"]
    },
    "MG": {
        "MG3": ["1.5", "1.5 Hybrid+"], "ZS": ["1.0 T-GDI", "1.5 VTi", "ZS EV"],
        "HS": ["1.5 T-GDI", "EHS Plug-in Hybrid"], "MG4": ["Standard Range", "Long Range", "XPower"]
    },
    "Mini": {
        "Cooper": ["Cooper", "Cooper S", "Cooper Electric"], "Countryman": ["Cooper", "Cooper S", "Cooper D", "SE ALL4"],
        "Clubman": ["Cooper", "Cooper S", "Cooper D"]
    },
    "Seat": {
        "Ibiza": ["1.0 MPI", "1.0 TSI", "1.6 TDI"], "Leon": ["1.0 TSI", "1.5 TSI", "2.0 TDI", "e-Hybrid"],
        "Arona": ["1.0 MPI", "1.0 TSI", "1.6 TDI"], "Ateca": ["1.5 TSI", "2.0 TSI", "2.0 TDI"]
    },
    "Skoda": {
        "Fabia": ["1.0 MPI", "1.0 TSI", "1.6 TDI"], "Scala": ["1.0 TSI", "1.5 TSI", "1.6 TDI"],
        "Octavia": ["1.5 TSI", "2.0 TDI", "iV"], "Superb": ["1.5 TSI", "2.0 TDI", "iV"],
        "Karoq": ["1.5 TSI", "2.0 TDI", "2.0 TSI"], "Kodiaq": ["1.5 TSI", "2.0 TDI", "iV"]
    },
    "Volvo": {
        "EX30": ["Single Motor", "Single Motor Extended Range", "Twin Motor Performance"],
        "XC40": ["T2", "B4", "Recharge Pure Electric"], "XC60": ["B5", "B6", "Recharge T8"],
        "XC90": ["B5", "B6", "Recharge T8"], "S60": ["B4", "B5", "Recharge T8"]
    }
}
 
depo_kapasiteleri = {
    "BMW": {"1 Serisi": 52, "2 Serisi": 52, "3 Serisi": 59, "4 Serisi": 60, "5 Serisi": 66, "6 Serisi": 70, "7 Serisi": 74, "8 Serisi": 68, "X1": 51, "X2": 51, "X3": 65, "X4": 65, "X5": 83, "X6": 83, "X7": 80},
    "Mercedes-Benz": {"A Serisi": 43, "B Serisi": 43, "C Serisi": 66, "E Serisi": 66, "S Serisi": 70, "CLA": 43, "GLA": 51, "GLB": 52, "GLC": 66, "GLE": 85, "GLS": 90},
    "Toyota": {"Yaris": 42, "Corolla": 50, "Camry": 50, "Auris": 50, "Avensis": 60, "C-HR": 43, "RAV4": 55, "Prius": 43, "Hilux": 80, "Land Cruiser": 93},
    "Volkswagen": {"Polo": 40, "Golf": 50, "Passat": 66, "Jetta": 55, "T-Roc": 50, "Tiguan": 58, "Touareg": 75},
    "Ford": {"Fiesta": 42, "Focus": 52, "Mondeo": 62, "Puma": 42, "Kuga": 54, "Mustang": 61},
    "Honda": {"Civic": 47, "Jazz": 40, "Accord": 65, "HR-V": 40, "CR-V": 57},
    "Nissan": {"Micra": 41, "Juke": 46, "Qashqai": 55, "X-Trail": 60, "Navara": 80},
    "Hyundai": {"i10": 36, "i20": 40, "i30": 50, "Elantra": 50, "Kona": 50, "Tucson": 54, "Santa Fe": 67},
    "Kia": {"Picanto": 35, "Rio": 45, "Ceed": 50, "Sportage": 54, "Niro": 45, "Sorento": 67},
    "Renault": {"Clio": 42, "Megane": 50, "Symbol": 50, "Captur": 48, "Austral": 55, "Kadjar": 55},
    "Peugeot": {"208": 44, "308": 53, "408": 52, "2008": 44, "3008": 53, "5008": 56},
    "Fiat": {"500": 35, "Panda": 37, "Egea": 50, "Tipo": 50, "Doblo": 60},
    "Opel": {"Corsa": 44, "Astra": 52, "Insignia": 62, "Mokka": 44, "Grandland": 53},
    "Mazda": {"Mazda2": 44, "Mazda3": 51, "Mazda6": 62, "CX-3": 48, "CX-30": 51, "CX-5": 58},
    "Audi": {"A1": 40, "A3": 50, "A4": 54, "A5": 54, "A6": 63, "A7": 63, "A8": 72, "Q2": 50, "Q3": 60, "Q5": 65, "Q7": 75, "Q8": 85},
    "Chery": {"Tiggo 4": 51, "Tiggo 7": 51, "Tiggo 8": 57},
    "Cupra": {"Formentor": 55, "Leon": 50, "Ateca": 55},
    "Jeep": {"Renegade": 48, "Compass": 60, "Cherokee": 60, "Grand Cherokee": 87},
    "Lexus": {"LBX": 36, "UX": 47, "NX": 55, "RX": 65, "ES": 50},
    "MG": {"MG3": 45, "ZS": 48, "HS": 55, "MG4": None},
    "Mini": {"Cooper": 44, "Countryman": 51, "Clubman": 48},
    "Seat": {"Ibiza": 40, "Leon": 50, "Arona": 40, "Ateca": 55},
    "Skoda": {"Fabia": 45, "Scala": 52, "Octavia": 50, "Superb": 66, "Karoq": 50, "Kodiaq": 58},
    "Volvo": {"EX30": None, "XC40": 54, "XC60": 71, "XC90": 71, "S60": 60}
}

# MARKA SEÇİMİ

marka_secimi = ttk.Combobox(
    arac_karti,
    values=list(modeller.keys()),
    state="readonly",
    width=36,
    style="Modern.TCombobox"
)
marka_secimi.pack(fill="x", pady=(0, 7))


# ARABA MODELİ

model_yazisi = tk.Label(
    arac_karti,
    text="Aracın modeli:",
    font=("Arial", 10, "bold"),
    bg="#FFFFFF",
    fg="#42627F"
)
model_yazisi.pack(anchor="w", pady=(0, 2))


model_secimi = ttk.Combobox(
    arac_karti,
    state="readonly",
    width=36,
    style="Modern.TCombobox"
)
model_secimi.pack(fill="x", pady=(0, 7))


# ARAÇ VERSİYONU

versiyon_yazisi = tk.Label(
    arac_karti,
    text="Araç versiyonu:",
    font=("Arial", 10, "bold"),
    bg="#FFFFFF",
    fg="#42627F"
)
versiyon_yazisi.pack(anchor="w", pady=(0, 2))


versiyon_secimi = ttk.Combobox(
    arac_karti,
    state="disabled",
    width=36,
    style="Modern.TCombobox"
)
versiyon_secimi.pack(fill="x", pady=(0, 7))


# MARKA SEÇİLDİĞİNDE MODELLERİ GETİR

def modelleri_goster(event):

    secilen_marka = marka_secimi.get()

    model_secimi["values"] = modeller[secilen_marka]

    model_secimi.set("")

    versiyon_secimi["values"] = []
    versiyon_secimi.set("")
    versiyon_secimi["state"] = "disabled"


def versiyonlari_goster(event):

    secilen_marka = marka_secimi.get()
    secilen_model = model_secimi.get()

    model_versiyonlari = versiyonlar.get(secilen_marka, {}).get(
        secilen_model, []
    )

    versiyon_secimi["values"] = model_versiyonlari
    versiyon_secimi.set("")
    versiyon_secimi["state"] = "readonly"


marka_secimi.bind(
    "<<ComboboxSelected>>",
    modelleri_goster
)
model_secimi.bind(
    "<<ComboboxSelected>>",
    versiyonlari_goster
)
# Aracın yılı

yil_yazisi = tk.Label(
    arac_karti,
    text="Aracın yılı:",
    font=("Arial", 10, "bold"),
    bg="#FFFFFF",
    fg="#42627F"
)
yil_yazisi.pack(anchor="w", pady=(0, 2))

yil_secimi = ttk.Combobox(
    arac_karti,
    values=list(range(1990, 2027)),
    state="readonly",
    width=36,
    style="Modern.TCombobox"
)
yil_secimi.pack(fill="x", pady=(0, 7))

# Yakıt türü 

yakit_turu = tk.Label(
    arac_karti,
    text="Yakıt türü:",
    font=("Arial", 10, "bold"),
    bg="#FFFFFF",
    fg="#42627F"
)
yakit_turu.pack(anchor="w", pady=(0, 2))

yakit_turleri = ["Benzin", "Dizel", "Elektrik", "Hibrit"]
yakit_secimi = ttk.Combobox(
    arac_karti,
    values=yakit_turleri,
    state="readonly",
    width=36,
    style="Modern.TCombobox"
)
yakit_secimi.pack(fill="x", pady=(0, 2))

# MEVCUT YAKIT

yakit_karti = tk.Frame(
    pencere,
    bg="#E8F4EF",
    highlightbackground="#B8DCCB",
    highlightthickness=1
)
yakit_karti.pack(fill="x", padx=28, pady=(0, 12))

yakit_yazisi = tk.Label(
    yakit_karti,
    text="MEVCUT YAKITIM",
    font=("Arial", 11, "bold"),
    bg="#E8F4EF",
    fg="#256B4F"
)
yakit_yazisi.pack(anchor="w", padx=16, pady=(12, 2))


yakit_seviyesi = tk.Scale(
    yakit_karti,
    from_=0,
    to=100,
    orient="horizontal",
    length=480,
    bg="#E8F4EF",
    fg="#256B4F",
    highlightthickness=0,
    troughcolor="#C7E6D7",
    activebackground="#2F936B"
)
yakit_seviyesi.set(50)
yakit_seviyesi.pack(fill="x", padx=12, pady=(0, 10))


def konumu_koordinata_cevir(konum):

    try:
        cevap = requests.get(
            "https://nominatim.openstreetmap.org/search",
            params={
                "q": konum,
                "format": "jsonv2",
                "limit": 1,
                "countrycodes": "tr"
            },
            headers={"User-Agent": "FuelRoute/1.0"},
            timeout=10
        )
        cevap.raise_for_status()
        sonuclar = cevap.json()

        if not sonuclar:
            return None

        return float(sonuclar[0]["lon"]), float(sonuclar[0]["lat"])

    except (requests.RequestException, ValueError, KeyError) as hata:
        print("Konum bilgisi alınırken hata oluştu:", hata)
        return False


def rota_mesafesini_hesapla(baslangic, varis):

    try:
        baslangic_lon, baslangic_lat = baslangic
        varis_lon, varis_lat = varis
        cevap = requests.get(
            "https://router.project-osrm.org/route/v1/driving/"
            f"{baslangic_lon},{baslangic_lat};{varis_lon},{varis_lat}",
            params={"overview": "full", "geometries": "geojson"},
            timeout=10
        )
        cevap.raise_for_status()
        rota_verisi = cevap.json()
        rotalar = rota_verisi.get("routes", [])

        if not rotalar:
            print("Rota bulunamadı.")
            return None

        rota = rotalar[0]
        geometri = rota.get("geometry", {}).get("coordinates", [])

        if not geometri:
            print("Rota geometrisi alınamadı.")
            return None

        return rota["distance"] / 1000, geometri

    except (requests.RequestException, ValueError, KeyError) as hata:
        print("Rota bilgisi alınırken hata oluştu:", hata)
        return None


def iki_nokta_arasi_mesafe_metre(nokta_1, nokta_2):

    lon_1, lat_1 = nokta_1
    lon_2, lat_2 = nokta_2
    yaricap = 6371000
    lat_fark = math.radians(lat_2 - lat_1)
    lon_fark = math.radians(lon_2 - lon_1)
    hesap = (
        math.sin(lat_fark / 2) ** 2
        + math.cos(math.radians(lat_1))
        * math.cos(math.radians(lat_2))
        * math.sin(lon_fark / 2) ** 2
    )
    return 2 * yaricap * math.asin(math.sqrt(hesap))


def rota_ornek_noktalari(geometri, aralik_metre=1500):

    ornekler = [geometri[0]]
    son_ornek = geometri[0]

    for nokta in geometri[1:-1]:
        if iki_nokta_arasi_mesafe_metre(son_ornek, nokta) >= aralik_metre:
            ornekler.append(nokta)
            son_ornek = nokta

    if geometri[-1] != ornekler[-1]:
        ornekler.append(geometri[-1])

    return ornekler


def rota_uzerindeki_istasyonlari_bul(geometri):

    try:
        ornekler = rota_ornek_noktalari(geometri)
        sorgu_noktalari = "\n".join(
            f'nwr["amenity"="fuel"](around:1500,{lat},{lon});'
            for lon, lat in ornekler
        )
        sorgu = f"[out:json][timeout:45];(\n{sorgu_noktalari}\n);out center tags;"
        cevap = requests.post(
            "https://overpass-api.de/api/interpreter",
            data={"data": sorgu},
            headers={"User-Agent": "FuelRoute/1.0"},
            timeout=60
        )
        cevap.raise_for_status()
        elemanlar = cevap.json().get("elements", [])

    except (requests.RequestException, ValueError, KeyError) as hata:
        return [], f"Benzinlik bilgileri alınırken hata oluştu: {hata}"

    rota_ilerlemeleri = [0]
    for onceki_nokta, sonraki_nokta in zip(geometri, geometri[1:]):
        rota_ilerlemeleri.append(
            rota_ilerlemeleri[-1]
            + iki_nokta_arasi_mesafe_metre(onceki_nokta, sonraki_nokta)
        )

    istasyonlar = []
    gorulenler = set()

    for eleman in elemanlar:
        istasyon_kimligi = (eleman.get("type"), eleman.get("id"))
        if istasyon_kimligi in gorulenler:
            continue

        gorulenler.add(istasyon_kimligi)
        merkez = eleman.get("center", eleman)
        if "lon" not in merkez or "lat" not in merkez:
            continue

        koordinat = (merkez["lon"], merkez["lat"])
        en_yakin_indeks, rotaya_uzaklik = min(
            enumerate(
                iki_nokta_arasi_mesafe_metre(koordinat, rota_noktasi)
                for rota_noktasi in geometri
            ),
            key=lambda sonuc: sonuc[1]
        )

        if rotaya_uzaklik > 750:
            continue

        etiketler = eleman.get("tags", {})
        istasyonlar.append({
            "ad": etiketler.get("name")
            or etiketler.get("brand")
            or etiketler.get("operator")
            or "İsimsiz akaryakıt istasyonu",
            "marka": etiketler.get("brand") or etiketler.get("operator"),
            "koordinat": koordinat,
            "rotaya_uzaklik_km": rotaya_uzaklik / 1000,
            "rota_ilerleme_km": rota_ilerlemeleri[en_yakin_indeks] / 1000
        })

    return sorted(istasyonlar, key=lambda istasyon: istasyon["rota_ilerleme_km"]), None


def rota_sonucunu_goster(
    nereden_bilgi, nereye_bilgi, marka_bilgi, model_bilgi, versiyon_bilgi,
    yil_bilgi, yakit_turu_bilgi, mesafe_km, tuketim, birim,
    tuketilecek_yakit, tuketim_birimi, mevcut_yakit_litre, yakit_yeterli,
    eksik_yakit, istasyonlar, istasyon_mesaji
):

    sonuc_penceresi = tk.Toplevel(pencere)
    sonuc_penceresi.title("FuelRoute - Rota Sonucu")
    sonuc_penceresi.geometry("520x760")
    sonuc_penceresi.configure(bg="#F4F7FB")
    sonuc_penceresi.resizable(False, False)
    sonuc_penceresi.transient(pencere)

    tk.Label(
        sonuc_penceresi,
        text="ROTA SONUCU",
        font=("Arial", 20, "bold"),
        bg="#F4F7FB",
        fg="#173B5C"
    ).pack(pady=(22, 4))

    tk.Label(
        sonuc_penceresi,
        text=f"{nereden_bilgi}  →  {nereye_bilgi}",
        font=("Arial", 11),
        bg="#F4F7FB",
        fg="#60758A",
        wraplength=410,
        justify="center"
    ).pack(padx=30, pady=(0, 16))

    bilgi_karti = tk.Frame(
        sonuc_penceresi,
        bg="#FFFFFF",
        highlightbackground="#DCE6F0",
        highlightthickness=1
    )
    bilgi_karti.pack(fill="x", padx=28)

    bilgiler = [
        ("ARAÇ", f"{marka_bilgi} {model_bilgi} {versiyon_bilgi}"),
        ("MODEL YILI", yil_bilgi),
        ("YAKIT TÜRÜ", yakit_turu_bilgi),
        ("MESAFE", f"{mesafe_km:.1f} km"),
        ("ORTALAMA TÜKETİM", f"{tuketim:.1f} {birim}"),
        ("TAHMİNİ TÜKETİM", f"{tuketilecek_yakit:.1f} {tuketim_birimi}")
    ]

    for baslik, deger in bilgiler:
        satir = tk.Frame(bilgi_karti, bg="#FFFFFF")
        satir.pack(fill="x", padx=14, pady=5)
        tk.Label(
            satir,
            text=baslik,
            font=("Arial", 9, "bold"),
            bg="#FFFFFF",
            fg="#60758A"
        ).pack(side="left")
        tk.Label(
            satir,
            text=deger,
            font=("Arial", 10),
            bg="#FFFFFF",
            fg="#173B5C",
            wraplength=235,
            justify="right"
        ).pack(side="right")

    if yakit_yeterli is None:
        durum_metni = "Elektrikli araçlarda batarya yeterliliği henüz hesaplanmıyor."
        durum_renk = "#5E6E80"
        durum_arka_plan = "#EAF0F5"
    elif yakit_yeterli:
        durum_metni = f"Yakıt yolculuk için yeterli.\nMevcut yakıt: {mevcut_yakit_litre:.1f} L"
        durum_renk = "#256B4F"
        durum_arka_plan = "#E8F4EF"
    else:
        durum_metni = (
            "Yakıt yolculuk için yeterli değil.\n"
            f"Mevcut yakıt: {mevcut_yakit_litre:.1f} L  •  Eksik yakıt: {eksik_yakit:.1f} L"
        )
        durum_renk = "#A83A3A"
        durum_arka_plan = "#FBEAEA"

    durum_karti = tk.Label(
        sonuc_penceresi,
        text=durum_metni,
        font=("Arial", 10, "bold"),
        bg=durum_arka_plan,
        fg=durum_renk,
        justify="center",
        wraplength=390,
        padx=16,
        pady=13
    )
    durum_karti.pack(fill="x", padx=28, pady=16)

    istasyon_karti = tk.Frame(
        sonuc_penceresi,
        bg="#FFFFFF",
        highlightbackground="#DCE6F0",
        highlightthickness=1
    )
    istasyon_karti.pack(fill="both", expand=True, padx=28)

    tk.Label(
        istasyon_karti,
        text="ROTA ÜZERİNDEKİ BENZİNLİKLER",
        font=("Arial", 10, "bold"),
        bg="#FFFFFF",
        fg="#173B5C"
    ).pack(anchor="w", padx=14, pady=(10, 4))

    if istasyon_mesaji:
        istasyon_metni = istasyon_mesaji
    elif not istasyonlar:
        istasyon_metni = "Rota üzerinde yakın bir akaryakıt istasyonu bulunamadı."
    else:
        istasyon_satirlari = []
        for istasyon in istasyonlar:
            baslik = istasyon["ad"]
            if istasyon["marka"] and istasyon["marka"] != baslik:
                baslik = f"{baslik} ({istasyon['marka']})"
            istasyon_satirlari.append(
                f"⛽ {baslik}\n"
                f"{istasyon['rota_ilerleme_km']:.1f} km sonra"
                f" • Rotaya {istasyon['rotaya_uzaklik_km']:.1f} km"
            )
        istasyon_metni = "\n\n".join(istasyon_satirlari)

    istasyon_yazisi = tk.Text(
        istasyon_karti,
        height=7,
        font=("Arial", 10),
        bg="#FFFFFF",
        fg="#304B63",
        relief="flat",
        wrap="word"
    )
    istasyon_yazisi.insert("1.0", istasyon_metni)
    istasyon_yazisi.configure(state="disabled")
    istasyon_yazisi.pack(fill="both", expand=True, padx=(14, 2), pady=(0, 10), side="left")

    istasyon_kaydirma = tk.Scrollbar(
        istasyon_karti,
        command=istasyon_yazisi.yview
    )
    istasyon_kaydirma.pack(fill="y", padx=(0, 10), pady=(0, 10), side="right")
    istasyon_yazisi.configure(yscrollcommand=istasyon_kaydirma.set)

    tk.Button(
        sonuc_penceresi,
        text="KAPAT",
        font=("Arial", 10, "bold"),
        bg="#1F7A5A",
        fg="#FFFFFF",
        activebackground="#176246",
        activeforeground="#FFFFFF",
        relief="flat",
        padx=22,
        pady=8,
        command=sonuc_penceresi.destroy
    ).pack(pady=(0, 20))


# ROTAYI HESAPLA

def rotayi_hesapla():

    nereden_bilgi = nereden.get()

    nereye_bilgi = nereye.get()

    marka_bilgi = marka_secimi.get()

    model_bilgi = model_secimi.get()
    versiyon_bilgi = versiyon_secimi.get()
    yakit_turu_bilgi = yakit_secimi.get()


    yakit_bilgi = yakit_seviyesi.get()


    # FORM KONTROLÜ

    if nereden_bilgi == "":

        print("Lütfen nereden gideceğinizi seçin.")

        return

    if nereye_bilgi == "":

        print("Lütfen nereye gideceğinizi seçin.")

        return

    if marka_bilgi == "":

        print("Lütfen araç markasını seçin.")

        return

    if model_bilgi == "":

        print("Lütfen araç modelini seçin.")

        return

    if versiyon_bilgi == "":

        print("Lütfen araç versiyonunu seçin.")

        return

    if yil_secimi.get() == "":

        print("Lütfen araç yılını seçin.")

        return

    if yakit_turu_bilgi == "":

        print("Lütfen yakıt türünü seçin.")

        return

    baslangic_koordinat = konumu_koordinata_cevir(nereden_bilgi)

    if baslangic_koordinat is False:

        return

    if baslangic_koordinat is None:

        print("Başlangıç konumu bulunamadı.")

        return

    varis_koordinat = konumu_koordinata_cevir(nereye_bilgi)

    if varis_koordinat is False:

        return

    if varis_koordinat is None:

        print("Varış konumu bulunamadı.")

        return

    rota_bilgisi = rota_mesafesini_hesapla(
        baslangic_koordinat, varis_koordinat
    )

    if rota_bilgisi is None:

        return

    mesafe_km, rota_geometrisi = rota_bilgisi

    tuketim = ortalama_tuketimler.get(marka_bilgi, {}).get(
        model_bilgi, {}
    ).get(yakit_turu_bilgi)

    if tuketim is None:

        print("Bu araç için seçilen yakıt türünde tüketim verisi bulunamadı.")

        return

    birim = "kWh/100 km" if yakit_turu_bilgi == "Elektrik" else "L/100 km"

    tuketilecek_yakit = (mesafe_km / 100) * tuketim
    tuketim_birimi = "kWh" if yakit_turu_bilgi == "Elektrik" else "L"

    mevcut_yakit_litre = None
    yakit_yeterli = None
    eksik_yakit = None

    if yakit_turu_bilgi != "Elektrik":

        depo_kapasitesi = depo_kapasiteleri.get(marka_bilgi, {}).get(
            model_bilgi
        )

        if depo_kapasitesi is None:

            print("Bu araç için depo kapasitesi verisi bulunamadı.")

            return

        mevcut_yakit_litre = depo_kapasitesi * (yakit_bilgi / 100)

        yakit_yeterli = mevcut_yakit_litre >= tuketilecek_yakit

        if not yakit_yeterli:

            eksik_yakit = tuketilecek_yakit - mevcut_yakit_litre

    istasyonlar, istasyon_mesaji = rota_uzerindeki_istasyonlari_bul(
        rota_geometrisi
    )

    rota_sonucunu_goster(
        nereden_bilgi, nereye_bilgi, marka_bilgi, model_bilgi,
        versiyon_bilgi, yil_secimi.get(), yakit_turu_bilgi, mesafe_km,
        tuketim, birim, tuketilecek_yakit, tuketim_birimi,
        mevcut_yakit_litre, yakit_yeterli, eksik_yakit,
        istasyonlar, istasyon_mesaji
    )
hesapla_butonu = tk.Button(

    pencere,

    text="ROTAYI HESAPLA",

    font=("Arial", 13, "bold"),

    bg="#1F7A5A",

    fg="#FFFFFF",

    activebackground="#176246",

    activeforeground="#FFFFFF",

    relief="flat",

    cursor="hand2",

    padx=24,

    pady=12,

    command=rotayi_hesapla

)

hesapla_butonu.pack(fill="x", padx=28, pady=(0, 18))
api_key = os.getenv("GOOGLE_MAPS_API_KEY")

print(".env bulundu:", env_dosyasi.exists())

print("API anahtarı bulundu:", api_key is not None)
url = "https://places.googleapis.com/v1/places:autocomplete"

headers = {

    "Content-Type": "application/json",

    "X-Goog-Api-Key": api_key

}

veri = {

    "input": "Balıkesir",

    "includedRegionCodes": ["tr"]

}

cevap = requests.post(

    url,

    headers=headers,

    json=veri

)

print("Google Places durum kodu:", cevap.status_code)

print("Google Places cevabı:", cevap.text[:500])
pencere.mainloop()
