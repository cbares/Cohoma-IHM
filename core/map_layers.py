
import folium
from folium.plugins import MousePosition
import xyzservices.providers as xyz

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
        opacity=.5,
        overlay=True,
        useCache=True,
        crossOrigin=True,
    ).add_to(folium_map)

    fmtr = "function(num) {return L.Util.formatNum(num, 7) + ' º ';};"
    MousePosition(position='topright', separator=' | Lat: ', prefix="Lng:",
                  lat_formatter=fmtr, lng_formatter=fmtr).add_to(folium_map)

    folium.Marker(
        location=start_coords,
        popup="Papa Delta",
        icon=folium.Icon(color="red",icon="truck-fast",prefix="fa"),
    ).add_to(folium_map)
    html = folium_map.get_root()
    html.render()
    return {"map": html.html.render(),
            "script": html.script.render(),
            "header": html.header.render(),
            "mapname": folium_map.get_name(),
            }

