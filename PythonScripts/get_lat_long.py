import sqlite3
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut

def add_lat_long_columns_if_not_exist(db_path):
    """
    Add latitude and longitude columns to the 'project_addresses' table if they don't exist.
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    # Check if columns already exist
    cursor.execute("PRAGMA table_info(project_addresses)")
    columns = [column[1] for column in cursor.fetchall()]
    if "latitude" not in columns:
        cursor.execute("ALTER TABLE project_addresses ADD COLUMN latitude REAL")
    if "longitude" not in columns:
        cursor.execute("ALTER TABLE project_addresses ADD COLUMN longitude REAL")
    conn.commit()
    conn.close()

def fetch_addresses_from_db(db_path):
    """
    Fetch all addresses from the database where latitude or longitude is NULL.
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, street, house_number, zip_code, town 
        FROM project_addresses 
        WHERE latitude IS NULL OR longitude IS NULL
    """)
    addresses = cursor.fetchall()
    conn.close()
    return addresses

def update_lat_long_in_db(db_path, row_id, latitude, longitude):
    """
    Update latitude and longitude for a specific address in the database.
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE project_addresses
        SET latitude = ?, longitude = ?
        WHERE id = ?
    """, (latitude, longitude, row_id))
    conn.commit()
    conn.close()

def get_lat_long(geolocator, address):
    """
    Convert an address into latitude and longitude using Nominatim.
    """
    full_address = f"{address[1]} {address[2]}, {address[3]} {address[4]}"
    try:
        location = geolocator.geocode(full_address, timeout=10)
        if location:
            return location.latitude, location.longitude
        else:
            print(f"Geocoding failed for address: {full_address}")
            return None, None
    except GeocoderTimedOut:
        print(f"Geocoding timed out for address: {full_address}")
        return None, None

def main():
    # Path to your SQLite database
    db_path = "project_addresses.db"

    # Initialize Nominatim geocoder
    geolocator = Nominatim(user_agent="address_geocoder")

    # Ensure latitude and longitude columns exist in the database
    add_lat_long_columns_if_not_exist(db_path)

    # Fetch addresses that need geocoding
    addresses = fetch_addresses_from_db(db_path)

    for address in addresses:
        row_id, street, house_number, zip_code, town = address
        latitude, longitude = get_lat_long(geolocator, (row_id, street, house_number, zip_code, town))
        if latitude is not None and longitude is not None:
            print(f"Updating Address ID {row_id}: {street} {house_number}, {zip_code} {town}, Latitude: {latitude}, Longitude: {longitude}")
            update_lat_long_in_db(db_path, row_id, latitude, longitude)

if __name__ == "__main__":
    main()
