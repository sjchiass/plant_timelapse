# Catgrass Timelapse

These scripts take photos of growing catgrass and post them here.

You can access the dashboard at <https://sjchiass.github.io/plant_timelapse/index.html>

## Requirements

I have the requirements in the `requirements.txt` file

```
python=3.9 plotly pyserial jinja2 pandas
```

`plotly` is used for graphs, `pyserial` is used to read from the USB-connecter Arduino, `jinja2` fills in the "dashboard" with images and data, and `pandas` is used for date and data manipulation.

## Running

I run these scripts on a Raspberry Pi with Raspbian installed. cronjobs run the data collection and the pushing to GitHub.

```
*/10 * * * * bash /home/pi/plant_timelapse/timelapse.sh >> /home/pi/myscript.log 2>&1
*/10 * * * * python3 /home/pi/plant_timelapse/log_sensors.py >> /home/pi/myscript.log 2>&1
5 12 * * * bash /home/pi/plant_timelapse/commit_push.sh >> /home/pi/myscript.log 2>&1
```

`timelapse.sh` runs `raspistill` to take photos. `log_sensors.py` uses pyserial to read data from the USB-attached Arduino. `commit_push.sh` just does a commit and push to GitHub to share the results.

## Neat things

Here are some cool things I found out while working on this.

### pandas does a good job with datetimes

The `.last()` method will filter your data for the last `x`. This could be `.last("24h")` to get all records from the last day. Assuming your datetimes are sorted ascending, you can also do `.last("24h").head(1)` to get the earliest record from the last day. Read more about it here: <https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.last.html>

There are also `.floor()`, `.ceil()` and `.round()` methods for evening out your datetimes. <https://pandas.pydata.org/docs/reference/api/pandas.DatetimeIndex.floor.html>

Finally, there are methods like `.day()`, `.hour()` and `.minute()` to extract these components of your datetimes. These can be used with `.groupby()` to do something like `.groupby(df["datetime"].hour)` to split your data. <https://pandas.pydata.org/docs/reference/api/pandas.DatetimeIndex.hour.html>

### jinja2 helps with basic pages

jinja2 can insert values into a template in every place identified by every double-bracket `{{ marker }}`.

You can insert text, image paths in `<img>` tags, and even feed the JSON for plotly charts.

jinja2 can also do for loops when given python lists: <https://jinja.palletsprojects.com/en/3.0.x/templates/#for> Some properties of the loop, such as `loop.index`, can be accessed from within the template.


