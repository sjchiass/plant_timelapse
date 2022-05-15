import os
import re
from pathlib import Path
from datetime import datetime
import shutil

Path("./plant_videos").mkdir(parents=True, exist_ok=True)

files = os.listdir("./captioned_images")

### Make weekly videos ###
pattern = re.compile("plant_(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}).jpg")

def extract_time(file, pattern):
    match = pattern.match(file)
    if match:
        return match.group(1)
    else:
        return None

datetimes = [extract_time(x, pattern) for x in files]
weeks = [datetime.fromisoformat(x).isocalendar().week for x in datetimes]
last_week = max(weeks)
file_weeks = dict()

for week in set(weeks):
    if week != last_week:
        file_weeks[week] = list()

for file, week in zip(files, weeks):
    if week != last_week:
        file_weeks[week].append(file)

for w in file_weeks.keys():
    Path("./weekly_images").mkdir(parents=True, exist_ok=True)
    for f in file_weeks[w]:
        shutil.copyfile("./captioned_images/"+f,
        "./weekly_images/"+f)
    os.system(
    f"ffmpeg -n -r 24 -hide_banner -loglevel error "+    # fps + verbosity
    f"-pattern_type glob -i './weekly_images/*.jpg' "+ # matching
    f"-vf yadif,format=yuv420p -c:v libx264 -preset slow -crf 18 "+
    f"-pix_fmt yuv420p ./plant_videos/{w}.mkv") # video output
    shutil.rmtree("./weekly_images")

