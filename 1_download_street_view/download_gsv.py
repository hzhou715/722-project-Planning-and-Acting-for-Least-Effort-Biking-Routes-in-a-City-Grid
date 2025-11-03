import requests
import os
import pandas as pd
from tqdm import tqdm  # Progress bar

# Replace with your API key
API_KEY = "xxx"

# Function to download Street View image
def download_street_view_image(panoid, heading, filename):
    url = f"https://maps.googleapis.com/maps/api/streetview?size=1024x512&pano={panoid}&heading={heading}&fov={fov}&pitch={pitch}&key={API_KEY}"
    response = requests.get(url)

    if response.status_code == 200:
        with open(filename, 'wb') as file:
            file.write(response.content)
        print(f"Downloaded {filename}")
    else:
        print(f"Failed to download {filename}")

# Parameters
headings = [0, 90, 180, 270]  # Different directions
fov = 90  # Field of view
pitch = 0  # Pitch

# Path to save images
save_directory = "patch"

# Create directory if it does not exist
if not os.path.exists(save_directory):
    os.makedirs(save_directory)

# Read CSV file to get Pano_IDs
csv_file_path = 'panoid_unique_latest_date.csv'
df = pd.read_csv(csv_file_path)

# Extract Pano_IDs
panoids = df['Pano_ID'].unique()

# Download images with a progress bar
for panoid in tqdm(panoids, desc="Downloading images"):
    for heading in headings:
        filename = os.path.join(save_directory, f"{panoid}_{heading}.jpg")
        download_street_view_image(panoid, heading, filename)