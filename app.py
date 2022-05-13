from flask import Flask
import folium
import json
import os

app = Flask(__name__)
geo_filename = os.path.join(app.static_folder, 'data', 'geo_map.json')


@app.route('/')
def index():
    with open(geo_filename) as geo_json_file:
        geo_data = json.load(geo_json_file)

    folium_map = folium.Map(
        location=[
            -31.61492,
            -64.74913
        ],
        tiles="OpenStreetMap",
        zoom_start=15,
    )
    folium.GeoJson(geo_data, name="geojson").add_to(folium_map)

    return folium_map._repr_html_()


if __name__ == '__main__':
    app.run()
