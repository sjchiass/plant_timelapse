import os
import re
from pathlib import Path

Path("./plant_videos").mkdir(parents=True, exist_ok=True)

# Create a regex pattern to definitively identify the files
pattern = re.compile("^plant_.*.jpg$")

# Since we're looking for all different days, we check the below string's
# length. By truncating all the filenames, we discard the hours, minutes
# and seconds.
day_pattern = "plant_xxxx_xx_xx"

# Get all of the files, only keep the stems
#files = os.listdir("./plant_stills")
files = os.listdir("./captioned_images")
day_stems = [x[:len(day_pattern)] for x in files if pattern.match(x)]

# Drop duplicate while keeping order, remove the last item (partial day)
day_stems = list(dict.fromkeys(day_stems))
day_stems.pop()
print(day_stems)

# We can feed each day into ffmpeg
# I break the command into multiple lines
for f in day_stems:
    os.system(
    f"ffmpeg -n -r 12 -hide_banner -loglevel error "+    # fps + verbosity
    f"-pattern_type glob -i './captioned_images/{f}*.jpg' "+ # matching
    f"-vf yadif,format=yuv420p -c:v libx264 -preset slow -crf 18 "+
    f"-pix_fmt yuv420p ./plant_videos/{f}.mkv") # video output

