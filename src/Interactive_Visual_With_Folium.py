import folium
import pandas as pd

# Import folium MarkerCluster plugin
from folium.plugins import MarkerCluster
# Import folium MousePosition plugin
from folium.plugins import MousePosition
# Import folium DivIcon plugin
from folium.features import DivIcon

## Task 1: Mark all launch sites on a map


# Download and read the `spacex_launch_geo.csv`
from js import fetch
import io

URL = 'https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/spacex_launch_geo.csv'
resp = await fetch(URL)
spacex_csv_file = io.BytesIO((await resp.arrayBuffer()).to_py())
spacex_df=pd.read_csv(spacex_csv_file)

# Select relevant sub-columns: `Launch Site`, `Lat(Latitude)`, `Long(Longitude)`, `class`
spacex_df = spacex_df[['Launch Site', 'Lat', 'Long', 'class']]
launch_sites_df = spacex_df.groupby(['Launch Site'], as_index=False).first()
launch_sites_df = launch_sites_df[['Launch Site', 'Lat', 'Long']]
launch_sites_df

# Start location is NASA Johnson Space Center
nasa_coordinate = [29.559684888503615, -95.0830971930759]
site_map = folium.Map(location=nasa_coordinate, zoom_start=10)

# Create a blue circle at NASA Johnson Space Center's coordinate with a popup label showing its name
circle = folium.Circle(nasa_coordinate, radius=1000, color='#d35400', fill=True).add_child(folium.Popup('NASA Johnson Space Center'))
# Create a blue circle at NASA Johnson Space Center's coordinate with a icon showing its name
marker = folium.map.Marker(
    nasa_coordinate,
    # Create an icon as a text label
    icon=DivIcon(
        icon_size=(20,20),
        icon_anchor=(0,0),
        html='<div style="font-size: 12; color:#d35400;"><b>%s</b></div>' % 'NASA JSC',
        )
    )
site_map.add_child(circle)
site_map.add_child(marker)

#TODO: Create and add folium.Circle and folium.Marker for each launch site on the site map
# Réinitialisation de la carte centrée sur le milieu des États-Unis avec un zoom adapté
site_map = folium.Map(location=[37.0902, -95.7129], zoom_start=4)

# Boucle à travers le DataFrame des sites uniques pour les placer sur la carte
for index, row in launch_sites_df.iterrows():
    coordinate = [row['Lat'], row['Long']]
    site_name = row['Launch Site']

    # 1. Création d'un cercle texturé autour du pas de tir
    circle = folium.Circle(
        location=coordinate,
        radius=1000,
        color='#d35400',
        fill=True,
        fill_color='#d35400',
        fill_opacity=0.4
    ).add_child(folium.Popup(site_name))

    # 2. Création d'un marqueur avec une étiquette textuelle (DivIcon) visible directement
    marker = folium.map.Marker(
        location=coordinate,
        icon=DivIcon(
            icon_size=(20, 20),
            icon_anchor=(0, 0),
            html=f'<div style="font-size: 12px; color:#d35400; font-weight: bold;">{site_name}</div>',
        )
    )

    # Ajout des éléments à la carte globale
    site_map.add_child(circle)
    site_map.add_child(marker)

# Initial the map
site_map = folium.Map(location=nasa_coordinate, zoom_start=5)
# For each launch site, add a Circle object based on its coordinate (Lat, Long) values. In addition, add Launch site name as a popup label


# Task 2: Mark the success/failed launches for each site on the map
# Task 2: Mark the success/failed launches for each site on the map
# 1. Création de l'objet MarkerCluster pour grouper les marqueurs trop proches
marker_cluster = MarkerCluster()


# 2. Fonction pour assigner une couleur selon la réussite de la mission
# Vert (green) pour un succès (1), Rouge (red) pour un échec (0)
def assign_marker_color(launch_class):
    if launch_class == 1:
        return 'green'
    else:
        return 'red'


# 3. Application de la fonction pour créer une nouvelle colonne de couleurs
spacex_df['marker_color'] = spacex_df['class'].apply(assign_marker_color)

# 4. Boucle pour ajouter chaque lancement du jeu de données global dans le cluster
for index, row in spacex_df.iterrows():
    coordinate = [row['Lat'], row['Long']]
    site_name = row['Launch Site']
    launch_status = "Success" if row['class'] == 1 else "Failure"

    # Création d'un marqueur d'icône coloré standard
    marker = folium.Marker(
        location=coordinate,
        icon=folium.Icon(color='white', icon_color=row['marker_color']),
        popup=folium.Popup(f"Site: {site_name}<br>Status: {launch_status}")
    )

    # On ajoute le marqueur directement au cluster, et non à la carte principale
    marker_cluster.add_child(marker)

# 5. Ajout du cluster complet à la carte principale
site_map.add_child(marker_cluster)

# Afficher la carte finale
site_map

#Next, let's try to enhance the map by adding the launch outcomes for each site, and see which sites have high success rates.
spacex_df.tail(10)

#Let's first create a MarkerCluster object
marker_cluster = MarkerCluster()


# 1. Fonction pour attribuer la couleur : vert pour un succès (1), rouge pour un échec (0)
def assign_marker_color(launch_class):
    if launch_class == 1:
        return 'green'
    else:
        return 'red'


# 2. Application de la fonction pour créer la colonne 'marker_color'
spacex_df['marker_color'] = spacex_df['class'].apply(assign_marker_color)

# 3. TODO : Ajouter chaque marqueur de lancement au cluster de marqueurs (MarkerCluster)
for index, row in spacex_df.iterrows():
    coordinate = [row['Lat'], row['Long']]

    # Création du marqueur individuel avec la couleur correspondante
    marker = folium.Marker(
        location=coordinate,
        icon=folium.Icon(color='white', icon_color=row['marker_color']),
        popup=f"Site: {row['Launch Site']}<br>Status: {'Success' if row['class'] == 1 else 'Failure'}"
    )

    # Ajout du marqueur au groupe (cluster)
    marker_cluster.add_child(marker)

# 4. Ajout du cluster d'icônes à la carte principale
site_map.add_child(marker_cluster)

# Affichage de la carte mise à jour
site_map

# TASK 3: Calculate the distances between a launch site to its proximities
# ==============================================================================
# TASK 3: Calculate the distances between a launch site to its proximities
# ==============================================================================

from math import sin, cos, sqrt, atan2, radians

def calculate_distance(lat1, lon1, lat2, lon2):
    # Rayon moyen de la Terre en kilomètres
    R = 6373.0

    lat1 = radians(lat1)
    lon1 = radians(lon1)
    lat2 = radians(lat2)
    lon2 = radians(lon2)

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c
    return distance

# --- 1. AJOUT DE L'OUTIL MOUSE POSITION POUR TROUVER LES COORDONNÉES (Optionnel mais recommandé) ---
formatter = "function(num) {return L.Util.formatNum(num, 5);};"
mouse_position = MousePosition(
    position='topright',
    separator=' Long: ',
    empty_string='NaN',
    lng_first=False,
    num_digits=20,
    prefix='Lat:',
    lat_formatter=formatter,
    lng_formatter=formatter,
)
site_map.add_child(mouse_position)

# --- 2. EXEMPLE : CALCUL DE DISTANCE VERS LA CÔTE LA PLUS PROCHE (Exemple : KSC LC-39A) ---

# Coordonnées du site de lancement (KSC LC-39A)
launch_site_lat = 28.57325
launch_site_lon = -80.64689

# Coordonnées du point de côte le plus proche (à trouver en survolant la carte avec votre souris)
coastline_lat = 28.57325
coastline_lon = -80.60669

# Calcul de la distance via la fonction Haversine
distance_coastline = calculate_distance(launch_site_lat, launch_site_lon, coastline_lat, coastline_lon)

# --- 3. AFFICHAGE DU MARQUEUR DE DISTANCE SUR LA CARTE ---
distance_marker = folium.Marker(
    [coastline_lat, coastline_lon],
    icon=DivIcon(
        icon_size=(20,20),
        icon_anchor=(0,0),
        html=f'<div style="font-size: 12px; color:#d35400; font-weight: bold;">{distance_coastline:.2f} KM</div>',
    )
)
site_map.add_child(distance_marker)

# --- 4. TRACER UNE LIGNE (POLYLINE) ENTRE LE SITE ET LA CÔTE ---
lines = folium.PolyLine(
    locations=[[launch_site_lat, launch_site_lon], [coastline_lat, coastline_lon]],
    weight=2,
    color='blue'
)
site_map.add_child(lines)

# Afficher la carte
site_map

# ==============================================================================
# TASK 3: Create markers and lines for Proximities (City, Railway, Highway)
# ==============================================================================

# Coordonnées du site de référence : KSC LC-39A
launch_site_lat = 28.57325
launch_site_lon = -80.64689

# Dictionnaire regroupant les coordonnées des infrastructures les plus proches
# (Trouvées à l'aide de l'outil MousePosition sur la carte)
proximities = {
    'Coastline': {'lat': 28.57325, 'lon': -80.60669, 'color': 'blue'},
    'Highway (Samuel C Phillips Pkwy)': {'lat': 28.57115, 'lon': -80.65545, 'color': 'green'},
    'Railroad': {'lat': 28.57314, 'lon': -80.65394, 'color': 'red'},
    'City (Titusville)': {'lat': 28.61200, 'lon': -80.80740, 'color': 'purple'}
}

# Boucle pour calculer la distance, ajouter le marqueur textuel et tracer la ligne pour chaque point
for name, coord in proximities.items():
    # 1. Calcul de la distance géodésique
    distance = calculate_distance(launch_site_lat, launch_site_lon, coord['lat'], coord['lon'])

    # 2. Création du marqueur affichant la distance en KM sur le point ciblé
    dist_marker = folium.Marker(
        location=[coord['lat'], coord['lon']],
        icon=DivIcon(
            icon_size=(150, 20),
            icon_anchor=(0, 0),
            html=f'<div style="font-size: 11px; color:{coord["color"]}; font-weight: bold;">'
                 f'{name}: {distance:.2f} KM</div>',
        ),
        popup=f"{name} - Distance: {distance:.2f} KM"
    )
    site_map.add_child(dist_marker)

    # 3. Tracé de la ligne brisée (PolyLine) reliant le pas de tir à l'infrastructure
    line = folium.PolyLine(
        locations=[[launch_site_lat, launch_site_lon], [coord['lat'], coord['lon']]],
        weight=2.5,
        color=coord['color'],
        opacity=0.8
    )
    site_map.add_child(line)

# Afficher à nouveau la carte avec toutes ses nouvelles liaisons
site_map