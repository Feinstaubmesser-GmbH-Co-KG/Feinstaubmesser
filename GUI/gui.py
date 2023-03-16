from customtkinter import *
from PIL import Image

# Fenster 1/2
root = CTk()

# Größe und Titel des Fensters
root.geometry("900x700")
root.title("Feinstaubmesser GmbH & Co. KG™")

# Spacing für Positionierung

# Labels definieren
info_text = CTkLabel(master=root, text="Willkommen zum Feinstaubmesser! \n"
                                       "In diesem Programm kannst du ein Datum eingeben und kriegst je \n"
                                       "nach Auswahl die Höchst-, Tiefst- oder Durchschnittswerte von \n"
                                       "Temperatur, Luftfeuchtigkeit und Feinstaubbelastung an dem Tag.")

typauswahl_text = CTkLabel(master=root, height=80,
                           text="Wähle ob du Temperatur, Luftfeuchtigkeit oder Feinstaubbelastung möchtest:")

wertauswahl_text = CTkLabel(master=root, height=80,
                            text="Wähle ob du Temperatur, Luftfeuchtigkeit oder Feinstaubbelastung möchtest:")
# Bilder einfügen
sonne = CTkImage(Image.open("Pics\Sonne.png"), size=(180, 180))
wolken = CTkImage(Image.open("Pics\Wolke.png"), size=(250, 250))
sonne_place = CTkLabel(master=root, image=sonne, text="", width=230, height=230)
wolke_place = CTkLabel(master=root, image=wolken, text="")

# Auswahl Typ
typauswahl = IntVar()
typauswahl.get()
temperatur = CTkRadioButton(master=root, text="Temperatur", variable=typauswahl, value=1)
feinstaubbelastung = CTkRadioButton(master=root, variable=typauswahl, value=2, text="Feinstaubbelastung")
luftfeuchtigkeit = CTkRadioButton(master=root, variable=typauswahl, value=3, text="Luftfeuchtigkeit")

# Auswahl Wert
wertauswahl = IntVar()
wertauswahl.get()
hoechster = CTkRadioButton(master=root, text="Höchster Wert", variable=wertauswahl, value=1)
tiefster = CTkRadioButton(master=root, variable=wertauswahl, value=2, text="Tiefster Wert")
durchschnitt = CTkRadioButton(master=root, variable=wertauswahl, value=3, text="Niedrigster Wert")

# Platzierungen
# # Info Texte
info_text.grid(row=0, column=1)
typauswahl_text.grid(row=1, column=1)
wertauswahl_text.grid(row=3, column=1)

# # Bilder
sonne_place.grid(column=0, row=0)
wolke_place.grid(column=2, row=5)

# # Typ Auswahl
temperatur.grid(row=2, column=0)
feinstaubbelastung.grid(row=2, column=1)
luftfeuchtigkeit.grid(row=2, column=2)

# # Wert Auswahl
hoechster.grid(row=4, column=0)
tiefster.grid(row=4, column=1)
durchschnitt.grid(row=4, column=2)

# Fenster 2/2
root.mainloop()
