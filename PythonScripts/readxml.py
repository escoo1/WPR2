import xml.etree.ElementTree as ET

# Pfad zur XML-Datei
xml_file = 'C:\\Users\\olive\\git\\WPR2\\xmlDocuments\\AM-DA50-0000001664.xml'

# XML-Datei parsen
tree = ET.parse(xml_file)
root = tree.getroot()

# Suche nach "projectAddress"
address_element = root.find('.//element[key="projectAddress"]/address')

if address_element is not None:
    street = address_element.find('street').text
    house_number = address_element.find('houseNumber').text
    zip_code = address_element.find('swissZipCode').text
    town = address_element.find('town').text

    # In ein anderes Dokument speichern (z.B. eine Textdatei)
    with open('project_address.txt', 'w') as f:
        f.write(f'Straße: {street}\n')
        f.write(f'Hausnummer: {house_number}\n')
        f.write(f'Postleitzahl: {zip_code}\n')
        f.write(f'Stadt: {town}\n')

    print("Adresse erfolgreich extrahiert und gespeichert.")
else:
    print("Adresse konnte nicht gefunden werden.")