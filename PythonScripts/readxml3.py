import os
import xml.etree.ElementTree as ET
import sqlite3
import shutil

# Funktion, um die entsprechenden Ordnerpfade zu bestimmen
def determine_folders():
    # Mögliche Pfade für den Benutzer 'olive'
    olive_xml_folder = 'C:\\Users\\olive\\git\\WPR2\\downloaded_xml_files\\'
    olive_processed_folder = 'C:\\Users\\olive\\git\\WPR2\\downloaded_xml_files\\'
    
    # Mögliche Pfade für den Benutzer 'lenobach'
    lenobach_xml_folder = '/Users/lenobach/git/WPR2/downloaded_xml_files'
    lenobach_processed_folder = '/Users/lenobach/git/WPR2/downloaded_xml_files'

    # Überprüfen, ob die Pfade von 'olive' existieren
    if os.path.exists(olive_xml_folder) and os.path.exists(olive_processed_folder):
        return olive_xml_folder, olive_processed_folder

    # Überprüfen, ob die Pfade von 'lenobach' existieren
    if os.path.exists(lenobach_xml_folder) and os.path.exists(lenobach_processed_folder):
        return lenobach_xml_folder, lenobach_processed_folder

    # Falls keine der Pfade existieren, einen Fehler auslösen
    raise FileNotFoundError("Neither 'olive' nor 'lenobach' folder paths exist.")

# Dynamisch die Ordnerpfade abrufen
xml_folder, processed_folder = determine_folders()

# Verbindung zur SQLite-Datenbank (erstellt eine neue Datei, wenn sie nicht existiert)
conn = sqlite3.connect('project_addresses.db')
cursor = conn.cursor()

# Erstellen der Tabelle, falls sie noch nicht existiert
cursor.execute('''
    CREATE TABLE IF NOT EXISTS project_addresses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        publication_id TEXT UNIQUE,
        street TEXT,
        house_number TEXT,
        zip_code TEXT,
        town TEXT,
        project_description TEXT
    )
''')

# Alle XML-Dateien im Ordner durchsuchen
for file_name in os.listdir(xml_folder):
    if file_name.endswith('.xml'):
        xml_file = os.path.join(xml_folder, file_name)

        try:
            # XML-Datei parsen
            tree = ET.parse(xml_file)
            root = tree.getroot()

            # Suche nach publication_id
            publication_id = root.find('.//publicationNumber').text if root.find('.//publicationNumber') is not None else None

            if publication_id is None:
                print(f"Keine publication_id in {file_name} gefunden.")
                continue

            # Suche nach Adressdaten in beiden Beispielen
            address_element = None

            # Suche nach der Adresse in projectAddress
            project_address = root.find('.//element[key="projectAddress"]/address')
            if project_address is not None:
                address_element = project_address
            else:
                # Suche nach der Adresse im projectLocation
                project_location = root.find('.//projectLocation/address')
                if project_location is not None:
                    address_element = project_location

            # Extrahieren der Adressdaten, falls address_element gefunden wurde
            if address_element is not None:
                street = address_element.find('street').text if address_element.find('street') is not None else None
                house_number = address_element.find('houseNumber').text if address_element.find('houseNumber') is not None else None
                zip_code = address_element.find('swissZipCode').text if address_element.find('swissZipCode') is not None else None
                town = address_element.find('town').text if address_element.find('town') is not None else None
            else:
                print(f"Adresse konnte in {file_name} nicht gefunden werden.")
                continue

            # Extrahieren der Projektbeschreibung
            project_description = None

            # Beispiel 1: Projektbeschreibung im Tag <projectDescription>
            project_description_element = root.find('.//projectDescription')
            if project_description_element is not None:
                project_description = project_description_element.text

            # Beispiel 2: Projektbeschreibung im Tag <valueText>
            if project_description is None:  # Wenn im ersten Schritt nichts gefunden wurde
                value_text_element = root.find('.//valueText/term/de')
                if value_text_element is not None:
                    project_description = value_text_element.text

            # Prüfen, ob die Adresse schon existiert
            cursor.execute('SELECT * FROM project_addresses WHERE publication_id = ?', (publication_id,))
            result = cursor.fetchone()

            if result is None:
                # Daten in die Datenbank einfügen
                cursor.execute('''
                    INSERT INTO project_addresses (publication_id, street, house_number, zip_code, town, project_description)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (publication_id, street, house_number, zip_code, town, project_description))

                print(f"Daten aus {file_name} erfolgreich in die Datenbank eingefügt.")
            else:
                print(f"Daten für {publication_id} bereits vorhanden.")

            # Datei in den Ordner 'processed' verschieben
            shutil.move(xml_file, os.path.join(processed_folder, file_name))
            print(f"{file_name} wurde nach 'processed' verschoben.")

        except ET.ParseError:
            print(f"Fehler beim Parsen der Datei: {file_name}")
        except Exception as e:
            print(f"Ein Fehler ist aufgetreten: {str(e)}")

# Änderungen speichern und Verbindung zur Datenbank schliessen
conn.commit()
conn.close()

print("Alle XML-Dateien wurden verarbeitet.")
