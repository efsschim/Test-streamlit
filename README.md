# Urban Monitoring Dashboard

Dieses Repository enthält ein Streamlit-Dashboard, das simulierte Messwerte zur Verkehrsauslastung
und Energieversorgung einer Stadt visualisiert. Es dient als Ausgangspunkt, um eigene Datenquellen
anzuschließen oder die Visualisierungen an projektspezifische Anforderungen anzupassen.

## Features

- 🚦 **Verkehr**: Fahrzeugaufkommen, Durchschnittsgeschwindigkeit und Stauindex mit Zeitreihen und
  Kartenansicht einzelner Sensoren.
- ⚡ **Energie**: Zusammensetzung der Stromerzeugung nach Quellen, Nachfrageentwicklung und
  Vergleich von Angebot und Verbrauch.
- 📊 **Vergleichswerkzeuge**: Filter für Zeitraum und Region sowie Gegenüberstellung von Werktagen
  und Wochenenden.

## Installation

1. Erstellen Sie am besten ein virtuelles Python-Umfeld (z. B. mit `venv`).
2. Installieren Sie die benötigten Pakete:

   ```bash
   pip install -r requirements.txt
   ```

   Falls nur Streamlit benötigt wird, genügt der Basiskommandozeilenaufruf:

   ```bash
   pip install streamlit
   ```

   Alternativ können Sie die Hauptabhängigkeiten manuell installieren:

   ```bash
   pip install streamlit pandas numpy altair
   ```

## Ausführen

Starten Sie das Dashboard lokal mit:

```bash
streamlit run app.py
```

Die App wird standardmäßig unter <http://localhost:8501> erreichbar sein. Verwenden Sie die Sidebar,
um Zeiträume, Regionen und Vergleichsansichten interaktiv zu steuern.

## Projekt-Smoke-Test ausführen

Zusätzlich können Sie einen schnellen Smoke-Test ohne Netzwerkzugriff starten. Dabei wird geprüft,
ob `app.py` syntaktisch gültig ist und ob die Kernabhängigkeiten in `requirements.txt` vorhanden sind:

```bash
python -m unittest tests/test_smoke.py
```

## Requirements-Test lokal ausführen

Um lokal zu prüfen, ob alle Abhängigkeiten installiert werden können, führen Sie im Projektverzeichnis
den Requirements-Test aus:

```bash
pip install -r requirements.txt
```

So lässt sich schnell nachvollziehen, ob das Setup auf Ihrem System vollständig ist.
