# Buchhaltungsdemo

Dieses Projekt enthält eine einfache Webanwendung für doppelte Buchhaltung auf Basis von Flask und SQLite. Die Anwendung liest die Konten aus `data/ekr.csv`. Dort kann der komplette österreichische Einheitskontenrahmen hinterlegt werden. Die mitgelieferte Datei enthält nur einen Auszug als Beispiel.

## Installation

```bash
pip install -r requirements.txt
python run.py
```

Beim ersten Start wird die Datenbank mit einigen Beispielkonten angelegt.

## Funktionen

* Erfassen von Buchungssätzen (Soll/Haben)
* Ansicht aller Konten
* Gewinn- und Verlustrechnung
* Bilanz
* Umsatzsteuervoranmeldung
* Modernes, responsives Frontend mit Vue unter `/vue_app`

Das Layout verwendet ein Bootswatch-Theme, wodurch die Anwendung auch auf Handy und Tablet gut aussieht.

Die Umsetzung dient nur als Demonstration und ist nicht für den produktiven Einsatz geeignet.
