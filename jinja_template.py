import jinja2
import pandas as pd
import os
import plotly
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import json
import os
import shutil
import re
from pathlib import Path

Path("./public").mkdir(parents=True, exist_ok=True)

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

# Get the latest time
latest_datetime = files_df.raw_time.tail(1).item()

# Get the hour of each file
files_df["hour"] = pd.to_datetime(files_df.raw_time).dt.floor("H")

# Get the last 12 hours, keep the first image for each hour
files_df = files_df.groupby("hour").first().last("12h")

# Get the image filenames into a list
filenames = files_df.filename.tolist()

# Copy these images for the website to display
for f in filenames:
  shutil.copyfile(f"./plant_stills/{f}", f"./public/{f}")

### Sensor Data ###
sensors_df = pd.read_csv("./sensor_data/data.csv",
  header=0,
  names=["time", "soil", "humidity", "temperature"])
sensors_df["dt"] = pd.to_datetime(sensors_df.time)
sensors_df = sensors_df.set_index("dt")
sensors_df = sensors_df.sort_index()

latest = sensors_df.tail(1)
previous = sensors_df.last("6h").head(1)

fig = go.Figure()

for n, (title, column) in enumerate(
    zip(["Soil moisture", "Humidity", "Temperature"],
        ["soil", "humidity", "temperature"])):
    fig.add_trace(go.Indicator(
        title = title,
        value = latest[column].item(),
        mode = "number+delta",
        delta = {'reference': previous[column].item()},
        gauge = {
            'axis': {'visible': False}},
        domain = {'row': 0, 'column': n}))

fig.update_layout(title="Sensor readings, compared to 6 hours ago",
                  grid = {'rows': 1, 'columns': 3, 'pattern': "independent"},
                  width=800, height=300)

indicators_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

last_24h = sensors_df.last("24h")

fig = make_subplots(specs=[[{"secondary_y": True}]])

fig.add_trace(go.Scatter(x=last_24h.index, y=sensors_df.soil, name="Soil moisture"), secondary_y=False)
fig.add_trace(go.Scatter(x=last_24h.index, y=last_24h.humidity, name="Humidity"), secondary_y=False)
fig.add_trace(go.Scatter(x=last_24h.index, y=last_24h.temperature, name="Temperature"), secondary_y=True)

fig.update_yaxes(title_text="Percentage", secondary_y=False, tickformat=".1f")
fig.update_yaxes(title_text="Celsius", secondary_y=True, tickformat=".1f")
fig.update_layout(title="Sensor readings over past 24 hours",
                  hovermode="x unified", width=800, height=300, template="simple_white")

time_series_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

index_template = (jinja2.Environment(
  loader=jinja2.FileSystemLoader("./")
  )
  .get_template("./template.html")
  .render(latest_datetime=latest_datetime,
          images=filenames,
          n_images=len(filenames),
          indicators=indicators_json,
          time_series=time_series_json)
  )

with open("./public/index.html", "w") as f:
  f.write(index_template)
