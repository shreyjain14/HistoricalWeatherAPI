import pandas as pd
from flask import Flask, render_template

app = Flask(__name__)

stations = pd.read_csv("weather_data/stations.txt", skiprows=17)
stations = stations[["STAID", "STANAME                                 ", "CN"]]


@app.route("/")
def home():
    return render_template("home.html", data=stations.to_html())


@app.route("/api/v1/<station>/<date>")
def about(station, date):
    station_fill = str(station).zfill(6)
    filename = f"weather_data/TG_STAID{station_fill}.txt"
    df = pd.read_csv(filename, skiprows=20, parse_dates=["    DATE"])
    temperature = df.loc[df['    DATE'] == date]['   TG'].squeeze() / 10
    return {"station": station,
            "date": date,
            "temperature": temperature}


@app.route("/api/v1/<station>")
def station_all(station):
    station_fill = str(station).zfill(6)
    filename = f"weather_data/TG_STAID{station_fill}.txt"
    df = pd.read_csv(filename, skiprows=20, parse_dates=["    DATE"])
    result = df.to_dict(orient="records")
    return result


@app.route("/api/v1/annual/<station>/<year>")
def yearly(station, year):
    station_fill = str(station).zfill(6)
    filename = f"weather_data/TG_STAID{station_fill}.txt"
    df = pd.read_csv(filename, skiprows=20)
    df["    DATE"] = df["    DATE"].astype(str)
    result = (df[df["    DATE"].str.startswith(str(year))].to_dict(orient="records"))
    return result


if __name__ == "__main__":
    app.run(debug=True)
