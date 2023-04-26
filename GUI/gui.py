from customtkinter import *
from PIL import Image
from database.api import SensorApi as api
from database import Configuration as config


def update():
    config.con.collect(config.db_url, config.db_port, config.db_schema_name, config.db_name, config.db_passwd)


# Fenster 1/2
root = CTk()

# Größe und Titel des Fensters
root.geometry("850x650")
root.title("Feinstaubmesser GmbH & Co. KG™")

# Spacing für Positionierung
spacing = CTkLabel(master=root, text="\n"
                                     "\n")

spacing2 = CTkLabel(master=root, text="\n")

# Labels definieren
info_text = CTkLabel(master=root, text="Willkommen zum Feinstaubmesser! \n"
                                       "In diesem Programm kannst du ein Datum eingeben und kriegst je \n"
                                       "nach Auswahl die Höchst-, Tiefst- oder Durchschnittswerte von \n"
                                       "Temperatur, Luftfeuchtigkeit und Feinstaubbelastung an dem Tag.")

typauswahl_text = CTkLabel(master=root, height=80,
                           text="Wähle ob du Temperatur, Luftfeuchtigkeit oder Feinstaubbelastung möchtest:")

wertauswahl_text = CTkLabel(master=root, height=80,
                            text="Wähle ob du Temperatur, Luftfeuchtigkeit oder Feinstaubbelastung möchtest:")

# Update Button
datenbank_update = CTkButton(master=root, text="Daten aktualisieren", command=update)

# Datumseingabe
datumseingabe = CTkEntry(master=root, placeholder_text="Datum bitte im Format: YYYY-MM-DD", width=217)

# Bilder einfügen
sonne = CTkImage(Image.open("Pics/Sonne.png"), size=(150, 150))
wolken = CTkImage(Image.open("Pics/Wolke.png"), size=(160, 100))
sonne_place = CTkLabel(master=root, image=sonne, text="", width=200, height=180)
wolke_place = CTkLabel(master=root, image=wolken, text="")

# Auswahl Typ
typauswahl = StringVar()
temperatur = CTkRadioButton(master=root, text="Temperatur", variable=typauswahl, value="Temperatur")
feinstaubbelastung = CTkRadioButton(master=root, variable=typauswahl, value="Feinstaubbelastung",
                                    text="Feinstaubbelastung")
luftfeuchtigkeit = CTkRadioButton(master=root, variable=typauswahl, value="Luftfeuchtigkeit", text="Luftfeuchtigkeit")

# Auswahl Wert
wertauswahl = StringVar()
hoechster = CTkRadioButton(master=root, variable=wertauswahl, value="Höchster Wert", text="Höchster Wert")
tiefster = CTkRadioButton(master=root, variable=wertauswahl, value="Tiefster Wert", text="Tiefster Wert")
durchschnitt = CTkRadioButton(master=root, variable=wertauswahl, value="Durchschnittlicher Wert",
                              text="Durchschnittlicher Wert")


# Auswahl bestätigen (Die 200 stellen sicher, dass die Ausgabe gelöscht wird) ;)
def auswahl_bes():
    ausgabe.delete("0.0", "200.0")
    text = ausgabe_gen()
    ausgabe.insert("0.0", text=text)


auswahl_gen = CTkButton(master=root, text="Auswahl bestätigen", command=auswahl_bes)


# Ausgabe
def ausgabe_gen():
    if datumseingabe.get() == "" or typauswahl.get() == "" or wertauswahl.get() == "":
        finale_ausgabe = "Bitte vervollständige deine Eingabe"
    else:
        sensor = None
        type = None

        if typauswahl.get() == "Temperatur":
            sensor = 3660
            type = "temperature"
        elif typauswahl.get() == "Feinstaubbelastung":
            sensor = 3659
            type = "P1"
        elif typauswahl.get() == "Luftfeuchtigkeit":
            sensor = 3660
            type = "humidity"

        result = api.get_sensor_data_by_date_type_and_value(sensor_id=sensor, date=datumseingabe.get(), type=type,
                                                            value=wertauswahl.get())
        text = ""
        for entry in result:
            if isinstance(entry, dict):
                for key, value in entry.items():
                    text += f"{value}"
            else:
                for list in entry:
                    for key, value in list.items():
                        k = key.replace("(", "").replace(")", "").replace("MIN", "").replace("MAX", "").replace("AVG",
                                                                                                                "")

                        text += f"{k}: {value} \n"

        return text

    return finale_ausgabe


ausgabe = CTkTextbox(master=root, width=150, height=50, border_width=2)

# Platzierungen
# # Info Texte + Datumseingabe
info_text.grid(row=0, column=1)
datumseingabe.grid(row=1, column=1, sticky="n")
typauswahl_text.grid(row=2, column=1)
wertauswahl_text.grid(row=5, column=1)

# # Update Button
datenbank_update.grid(row=0, column=2, sticky="ne", pady=10)

# # Bilder
sonne_place.grid(column=0, row=0)
wolke_place.grid(column=2, row=9)

# # Typ Auswahl
temperatur.grid(row=3, column=0, sticky="e")
feinstaubbelastung.grid(row=3, column=1)
luftfeuchtigkeit.grid(row=3, column=2, sticky="w")

# # Wert Auswahl
hoechster.grid(row=6, column=0, sticky="e")
tiefster.grid(row=6, column=1)
durchschnitt.grid(row=6, column=2, sticky="w")

# # Auswahl bestätigen
auswahl_gen.grid(row=8, column=1, sticky="s")

# # Ausgabe
ausgabe.grid(row=9, column=1)

# # Spacing
spacing.grid(row=4, column=1)
spacing2.grid(row=7, column=1)

# Fenster 2/2
root.mainloop()
