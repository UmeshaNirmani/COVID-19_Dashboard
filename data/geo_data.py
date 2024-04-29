import csv
import json

csv_file_path = "F:\study\projects\COVID-19 Dashboard - Power BI\COVID-19_Dashboard\data\District and MOH cases.csv"
json_file_path = "F:\study\projects\COVID-19 Dashboard - Power BI\COVID-19_Dashboard\data\geo_data.json"

# Open CSV file in read mode with 'utf-8' encoding (adjust if needed)
with open(csv_file_path, 'r', encoding='utf-8') as csvfile:
  # Create a DictReader object to access data by column names
  reader = csv.DictReader(csvfile)

  # Initialize an empty list to store GeoJSON features
  data = []

  # Check if CSV has latitude and longitude columns
  has_lat_lon = 'latitude' in reader.fieldnames and 'longitude' in reader.fieldnames

  # Loop through each row in the CSV file
  for row in reader:
    if has_lat_lon:
      # Scenario 1: With latitude and longitude columns
      feature = {
        "type": "Feature",
        "geometry": {
          "type": "Point",  # Replace "Point" with "LineString" or "Polygon" if applicable
          "coordinates": [float(row["longitude"]), float(row["latitude"])]
        },
        "properties": row  # Add all other columns from the row as properties
      }
    else:
      # Scenario 2: Without latitude and longitude columns (further processing needed)
      # Replace this section with your logic to convert data to GeoJSON features
      # (e.g., using geocoding or spatial data libraries)
      print(f"Warning: Missing latitude and longitude columns in row {row}")
      continue  # Skip this row if processing fails

    # Append feature object to data list
    data.append(feature)

# Open JSON file in write mode with 'utf-8' encoding (adjust if needed)
with open(json_file_path, 'w', encoding='utf-8') as jsonfile:
  # Write the list of GeoJSON features to the JSON file with indentation
  json.dump({"type": "FeatureCollection", "features": data}, jsonfile, indent=4)

print(f"GeoJSON file created and saved to: {json_file_path}")
