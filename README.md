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

   Alternativ können Sie die Hauptabhängigkeiten manuell installieren:

   ```bash
   pip install streamlit pandas numpy altair
   ```

## Ausführen

Starten Sie das Dashboard lokal mit:

```bash
streamlit run app.py
`````

Die App wird standardmäßig unter <http://localhost:8501> erreichbar sein. Verwenden Sie die Sidebar,
um Zeiträume, Regionen und Vergleichsansichten interaktiv zu steuern.
