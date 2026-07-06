import osmnx as ox
import pandas as pd
import random
from pathlib import Path

# ------- telling osmx to search for this place !!! -------
PLACE_NAME = "Foz do Iguaçu, Paraná, Brazil"

#-------- Download only places that are hospitals, clinics, or pharmacies.-----------
tags = {
    "amenity": [
        "hospital",
        "clinic",
        "pharmacy"
    ]
}

print("Downloading healthcare locations...")

healthcare = ox.features_from_place(
    PLACE_NAME,
    tags
)

# Keeping only columns that fits my case
healthcare = healthcare[
    ["name", "amenity", "geometry"]
].copy()

# get rid of the rows that dont have a name
healthcare = healthcare.dropna(subset=["name"])

#renamingh the aminity colum 
healthcare = healthcare.rename(columns={
    "amenity": "type"
})

# Convert all geometries to their centroid
healthcare["geometry"] = healthcare.geometry.centroid

# Extract latitude and longitude
healthcare["latitude"] = healthcare.geometry.y
healthcare["longitude"] = healthcare.geometry.x

# Keep only the final columns
healthcare = healthcare[
    [
        "name",
        "type",
        "latitude",
        "longitude"
    ]
]

delivery_types = [
    "Medicine",
    "Vaccine",
    "Blood Sample",
    "Medical Equipment"
]
# note to self/me that 1 is normal priority, 2 is medium priority, and 3 is high priority
def assign_priority(location_type):
    if location_type == "hospital":
        return 3

    elif location_type == "clinic":
        return 3

    elif location_type == "pharmacy":
        return random.choice([1, 2])

    else:
        return 1

healthcare["priority"] = healthcare["type"].apply(assign_priority)

#----------------------------------------------------------------------

def assign_weight(location_type):

    if location_type == "hospital":
        return random.randint(8, 15)

    elif location_type == "clinic":
        return random.randint(5, 10)

    elif location_type == "pharmacy":
        return random.randint(1, 5)

    return random.randint(1, 3)


healthcare["package_weight"] = healthcare["type"].apply(assign_weight)

#----------------------------------------------------------------------

healthcare["delivery_type"] = [
    random.choice(delivery_types)
    for _ in range(len(healthcare))
]

#----------------------------------------------------------------------

healthcare["service_time"] = [
    random.randint(5, 20)
    for _ in range(len(healthcare))
]

# Reset OpenStreetMap index
healthcare = healthcare.reset_index(drop=True)

# Create our own sequential ID
healthcare.insert(0, "id", range(1, len(healthcare) + 1))

print(healthcare.head(20))

print("\nDataset Summary")

print(healthcare.info())

# Create project data folder path
output_file = Path(__file__).resolve().parent.parent / "data" / "foz_healthcare_locations.csv"

healthcare.to_csv(
    output_file,
    index=False,
    encoding="utf-8-sig"
)

print(f"\nDataset saved successfully!")
print(f"Saved to: {output_file}")