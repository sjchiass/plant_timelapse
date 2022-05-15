import os
import pandas as pd
import re
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from pathlib import Path

Path("./captioned_images").mkdir(parents=True, exist_ok=True)

### Sensor Readings ###
# First read the data CSV and name its columns
data_df = pd.read_csv("./sensor_data/data.csv",
  header=0,
  names=["time", "soil", "humidity", "temperature"])

# Round every observation to the nearest 10 minute mark (for joining)
data_df = data_df.assign(time = pd.to_datetime(data_df.time).round("10min"))

### Image Filenames ###
# Get all filenames from the raw images' folder
files = os.listdir("./plant_stills")

# Create a regex pattern for extracting the ISO9001 datetime
pattern = re.compile("plant_(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}).jpg")

# If we can match a datetime, return it; otherwise, None
def extract_time(file, pattern):
    match = pattern.match(file)
    if match:
        return match.group(1)
    else:
        return None

# Build a dataframe with the extracted times
files_df = pd.DataFrame({"filename" : files,
                         "raw_time" : [extract_time(x, pattern) for x in files]})

# Round them to the nearest 10 minute mark
files_df = files_df.assign(time = pd.to_datetime(files_df.raw_time).round("10min"))

# Perform a left merge with the sensor data
# This will join them on the 10 minute mark
# If there is no match, the image has no sensor data
merged_df = files_df.merge(data_df, how="left")

### Captions ###
# Given an image filename, caption it, and save it elsewhere
def caption_image(filename, raw_time, soil, humidity, temperature):
    img = Image.open(f"./plant_stills/{filename}")
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("DejaVuSans.ttf", 32)
    draw.multiline_text(xy=(0, 0),
                        text=f"{raw_time}\n"+
                        f"Soil\n {soil:.2f}%\n"+
                        f"Humidity\n {humidity:.2f}%\n"+
                        f"Temperature\n {temperature:.2f}C",
                        fill="red",
                        font=font)
    img.save(f"./captioned_images/{filename}")

for row in merged_df.itertuples():
    caption_image(row.filename, row.raw_time, row.soil, row.humidity, row.temperature)
