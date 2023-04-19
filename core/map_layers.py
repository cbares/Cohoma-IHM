import folium
from folium.plugins import MousePosition
import xyzservices.providers as xyz

from db.repository.baptemes import filter_baptemes, names_baptemes
from db.session import get_db

#tiles = xyz.GeoportailFrance.orthos
tiles_plan = xyz.GeoportailFrance.plan
tiles_contour = xyz.GeoportailFrance.Elevation_Contour_Line
tiles = xyz.GeoportailFrance.Hr_Orthoimagery_Orthophotos
#tiles = xyz.GeoportailFrance.Orthoimagery_Orthophotos_Bdortho

def get_map_layers(start_coords, zoom):
    folium_map = folium.Map(
        tiles=None,
        location=start_coords,
        zoom_start=zoom,
        control_scale=True,
    )

    folium.TileLayer(
        name="ortho",
        min_zoom=0,
        max_zoom=22,
        max_native_zoom=tiles.max_zoom,
        tiles=tiles.build_url(),
        attr=tiles.html_attribution,
        useCache=True,
        crossOrigin=True,
    ).add_to(folium_map)

    folium.TileLayer(
        name="plan",
        min_zoom=0,
        max_zoom=22,
        max_native_zoom=tiles_plan.max_zoom,
        tiles=tiles_plan.build_url(),
        attr=tiles_plan.html_attribution,
        opacity=.5,
        overlay=True,
        useCache=True,
        crossOrigin=True,
    ).add_to(folium_map)

    folium.TileLayer(
        name="contour",
        min_zoom=0,
        max_zoom=22,
        max_native_zoom=tiles_contour.max_zoom,
        tiles=tiles_contour.build_url(),
        attr=tiles_contour.html_attribution,
        opacity=1,
        overlay=True,
        useCache=True,
        crossOrigin=True,
    ).add_to(folium_map)

    fmtr = "function(num) {return L.Util.formatNum(num, 7) + ' º ';};"
    MousePosition(position='topright', separator=' | Lat: ', prefix="Lng:",
                  lat_formatter=fmtr, lng_formatter=fmtr).add_to(folium_map)

    add_poi_to_map(folium_map)

    html = folium_map.get_root()
    html.render()
    return {"map": html.html.render(),
            "script": html.script.render(),
            "header": html.header.render(),
            "mapname": folium_map.get_name(),
            }


def add_poi_to_map(folium_map):
    POI_conf = {
        "PI": "green",
        "O1": "red",
        "T1": "lightblue",
        "T2": "blue",
        "T3": "darkblue",
        "T4": "purple",
        "LIMITE": "red",
        "LIMA-D": "green",
        "LIMA-1": "lightblue",
        "LIMA-2": "blue",
        "LIMA-3": "darkblue",
        "ZT": "orange",
        "RFA": "darkblue",
        "ROZ": "red",
        "ZC": "darkgreen",
    }

    db = next(get_db())
    for name in names_baptemes(db):
        points = filter_baptemes(name, db)
        type = points[0].type
        vertices = [(p.latitude, p.longitude) for p in points]

        if type == "point":
            color = POI_conf.get(name[0:2], "white")
            div = folium.DivIcon(html=(
                f'<svg height="100" width="100">'
                f'<line x1="35" y1="50" x2="65" y2="50" stroke="{color}" stroke-width="2" fill="none" />'
                f'<line x1="50" y1="35" x2="50" y2="65" stroke="{color}" stroke-width="2" fill="none" />'
                f'<text x="52" y="48" font-size="20" fill="{color}">{name}</text>'
                f'</svg>'),
                icon_anchor=(50, 50),
            )
            folium.Marker(
                location=vertices[0],
                #popup=name,
                icon=div,
                #icon=folium.Icon(color=color, icon="info", prefix="fa"),
            ).add_to(folium_map)

        if type == "ligne":
            color = POI_conf.get(name[0:6], "red")
            folium.PolyLine(
                locations=vertices,
                tooltip=name,
                color=color
            ).add_to(folium_map)

            div = folium.DivIcon(html=(
                f'<svg height="100" width="200">'
                f'<text x="53" y="50" font-size="20" dominant-baseline="middle" fill="{color}">{name}</text>'
                f'</svg>'),
                icon_anchor=(50, 50),
            )
            if name.startswith("LIMA"):
                folium.Marker(
                    location=vertices[0],
                    icon=div,
                ).add_to(folium_map)

        if type == "zone":
            tooltip = {
                "ZT": "Zone Techinque",
                "RFA": "Restricted Fly Area",
                "ROZ": "Restricted Operation Zone",
                "ZC": "Zone Contaminee",
            }
            color = POI_conf.get(name, "red")
            folium.Polygon(
                locations=vertices,
                tooltip=tooltip[name],
                color=color,
                fill=True,
            ).add_to(folium_map)
