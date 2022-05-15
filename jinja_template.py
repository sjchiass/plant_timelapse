import jinja2
import pandas as pd
import os

last_capture = sorted(os.listdir("./plant_stills"))[-1]

df = pd.read_csv("./sensor_data/data.csv",
  header=0,
  names=["time", "soil", "humidity", "temperature"]).tail(1)

index_template = (jinja2.Environment(
  loader=jinja2.FileSystemLoader("./")
  )
  .get_template("template.html")
  .render(last_capture=last_capture,
          time=df.time.item(),
          soil=df.soil.item(),
          humidity=df.humidity.item(),
          temperature=df.temperature.item())
  )

with open("index.html", "w") as f:
  f.write(index_template)
