import sqlite3
import folium

def fetch_coordinates_from_db(db_path):
    """
    Fetch all latitude and longitude data from the database.
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT street, house_number, zip_code, town, latitude, longitude
        FROM project_addresses
        WHERE latitude IS NOT NULL AND longitude IS NOT NULL
    """)
    data = cursor.fetchall()
    conn.close()
    return data

def create_map(coordinates, output_file="display_map.html"):
    """
    Create a folium map with markers for each coordinate.
    """
    if not coordinates:
        print("No coordinates found in the database.")
        return

    # Create a map centered on the first coordinate
    first_coordinate = coordinates[0]
    map_center = [first_coordinate[4], first_coordinate[5]]  # Latitude and Longitude
    folium_map = folium.Map(location=map_center, zoom_start=12)

    # Add a marker for each coordinate
    for entry in coordinates:
        street, house_number, zip_code, town, latitude, longitude = entry
        address = f"{street} {house_number}, {zip_code} {town}"
        folium.Marker(
            location=[latitude, longitude],
            popup=address,
            icon=folium.Icon(color="blue", icon="info-sign"),
        ).add_to(folium_map)

    # Save the map to an HTML file
    folium_map.save(output_file)
    print(f"Map has been saved to {output_file}. Open it in your browser to view.")

def main():
    # Path to your SQLite database
    db_path = "project_addresses.db"

    # Fetch coordinates from the database
    coordinates = fetch_coordinates_from_db(db_path)

    # Create and display the map
    create_map(coordinates)

if __name__ == "__main__":
    main()
