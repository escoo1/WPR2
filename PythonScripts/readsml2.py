import os
import xml.etree.ElementTree as ET
import sqlite3

# Pfad zum Ordner mit den XML-Dateien
xml_folder = 'C:\\Users\\olive\\git\\WPR2\\xmlDocuments\\'

# Verbindung zur SQLite-Datenbank (erstellt eine neue Datei, wenn sie nicht existiert)
conn = sqlite3.connect('project_addresses.db')
cursor = conn.cursor()

# Erstellen der Tabelle, falls sie noch nicht existiert
cursor.execute('''
    CREATE TABLE IF NOT EXISTS project_addresses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        street TEXT,
        house_number TEXT,
        zip_code TEXT,
        town TEXT
    )
''')

# Alle XML-Dateien im Ordner durchsuchen
for file_name in os.listdir(xml_folder):
    if file_name.endswith('.xml'):
        xml_file = os.path.join(xml_folder, file_name)

        # XML-Datei parsen
        tree = ET.parse(xml_file)
        root = tree.getroot()

        # Suche nach "projectAddress"
        address_element = root.find('.//element[key="projectAddress"]/address')

        if address_element is not None:
            street = address_element.find('street').text if address_element.find('street') is not None else None
            house_number = address_element.find('houseNumber').text if address_element.find('houseNumber') is not None else None
            zip_code = address_element.find('swissZipCode').text if address_element.find('swissZipCode') is not None else None
            town = address_element.find('town').text if address_element.find('town') is not None else None

            # Daten in die Datenbank einfügen
            cursor.execute('''
                INSERT INTO project_addresses (street, house_number, zip_code, town)
                VALUES (?, ?, ?, ?)
            ''', (street, house_number, zip_code, town))

            print(f"Daten aus {file_name} erfolgreich in die Datenbank eingefügt.")
        else:
            print(f"Adresse konnte in {file_name} nicht gefunden werden.")

# Änderungen speichern und Verbindung zur Datenbank schließen
conn.commit()
conn.close()

print("Alle XML-Dateien wurden verarbeitet.")
