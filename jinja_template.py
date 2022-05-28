"""
This script reads ./plant_stills and ./sensor_data so that it can 
populate the template.html with jinja2.

Usage: python ./jinja_template.py

The script starts by finding images from the last 12 hours and only
keeping one for each of these hours.

The CSV with the sensor data is then read to create plotly charts, which
are saved as JSON in the HTML page.

Finally, all this data is fed through jinja2 to make the index.html.
"""
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

#%% Image Filenames
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
files_df["dt"] = pd.to_datetime(files_df.raw_time)
files_df = files_df.set_index("dt")
files_df = files_df.sort_index()

# Get the latest time, to display on the page
latest_datetime = files_df.raw_time.tail(1).item()

# Get the hour of each file
files_df["hour"] = pd.to_datetime(files_df.raw_time).dt.floor("H")

# Get the last 12 hours, keep the first image for each hour
files_df = files_df.groupby("hour").first().last("12h")

# Get the image filenames into a list so that the website can refer to
# them all.
filenames = files_df.filename.tolist()

# Copy these images for the website to use
for f in filenames:
  shutil.copyfile(f"./plant_stills/{f}", f"./public/{f}")

#%% Sensor Data
# Read in data, add column headers, and set a datetime index
sensors_df = pd.read_csv("./sensor_data/data.csv",
  header=0,
  names=["time", "soil", "humidity", "temperature"])
sensors_df["dt"] = pd.to_datetime(sensors_df.time)
sensors_df = sensors_df.set_index("dt")
sensors_df = sensors_df.sort_index()

#%% Indicators
# Indicators are often used for KPIs, here we use them to summarise
# changes in sensor readings in the past 6 hours
# Determine the latest data and that of 6 hours ago
latest = sensors_df.tail(1)
previous = sensors_df.last("6h").head(1)

fig = go.Figure()

# For column, we want an indicator with a specific title
# The enumerate is used to place each indicator in a column in the grid
variables = ["Soil moisture", "Humidity", "Temperature"]
titles = ["soil", "humidity", "temperature"]
for n, (t, v) in enumerate(zip(variables, titles)):
    fig.add_trace(go.Indicator(
        title = t,
        value = latest[v].item(),
        mode = "number+delta",
        delta = {'reference': previous[v].item()},
        gauge = {
            'axis': {'visible': False}},
        domain = {'row': 0, 'column': n}))

# Define the grid and make the indicators smaller
fig.update_layout(title="Sensor readings, compared to 6 hours ago",
                  grid = {'rows': 1, 'columns': len(variables), 'pattern': "independent"},
                  width=800, height=300)

# Save the plot as a JSON string so that it can be used with plotly JS
indicators_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

#%% Time series
# Extract the last 7 days
last_7d = sensors_df.last("7d")

# Average the hours
last_7d = last_7d.resample("h").mean()

# Specify that the graph will have a secondary axis
# The main axis will be in % and the secondary axis degrees celsius
fig = make_subplots(specs=[[{"secondary_y": True}]])

# Add each trace
fig.add_trace(go.Scatter(x=last_7d.index, y=last_7d.soil, name="Soil moisture"), secondary_y=False)
fig.add_trace(go.Scatter(x=last_7d.index, y=last_7d.humidity, name="Humidity"), secondary_y=False)
fig.add_trace(go.Scatter(x=last_7d.index, y=last_7d.temperature, name="Temperature"), secondary_y=True)

# Add axis titles and set decimal places
fig.update_yaxes(title_text="Percentage", secondary_y=False, tickformat=".1f")
fig.update_yaxes(title_text="Celsius", secondary_y=True, tickformat=".1f")

# Change the hovermode to "x unified" which hovers over all variables at
# once. Also, use the "simple_white" theme that gets rid of all grid lines.
fig.update_layout(title="Sensor readings over past 7 days",
                  hovermode="x unified", width=800, height=300, template="simple_white")

# Save the plot as a JSON string so that it can be used with plotly JS
time_series_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

#%% Applying the template
# Jinja lets us fill in spots of an html template file. This way various
# information is put into the webpage
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

# Save the html
with open("./public/index.html", "w") as f:
  f.write(index_template)
