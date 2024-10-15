import os

# Pfad zur SQLite-Datenbank
db_path = 'project_addresses.db'

# Überprüfen, ob die Datenbankdatei existiert
if os.path.exists(db_path):
    try:
        # Löschen der Datei
        os.remove(db_path)
        print(f"Datenbank '{db_path}' erfolgreich gelöscht.")
    except Exception as e:
        print(f"Ein Fehler ist aufgetreten: {str(e)}")
else:
    print(f"Datenbank '{db_path}' existiert nicht.")
