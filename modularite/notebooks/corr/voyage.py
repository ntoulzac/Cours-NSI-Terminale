"""Ce module permet de représenter sur une carte de France un lieu ou des itinéraires à partir d'adresses."""

import requests
import folium

def _coord_BAN(lieu):
    """
    Détermine les coordonnées d'un lieu à partir d'une adresse, via l'API *Base Adresse Nationale*.
    - Entrée : lieu (couple au format (adresse, code_postal) où adresse est une chaîne et code_postal un entier)
    - Sortie : tableau au format [latitude, longitude] où latitude et longitude sont des flottants
    """
    adresse, code_postal = lieu[0], lieu[1]
    url = f"https://api-adresse.data.gouv.fr/search/?q={adresse}&postcode={code_postal}"
    reponse = requests.get(url)
    reponse = reponse.json()
    coord = reponse["features"][0]["geometry"]["coordinates"]
    return [coord[1], coord[0]]

def _itineraire_IGN(dep, arr):
    """
    Détermine l'itinéraire le plus court entre deux lieux, via l'API *Itinéraires* de l'IGN.
    - Entrée : dep, arr (tableaux au format [latitude, longitude] où latitude et longitude sont des flottants)
    - Sortie : dictionnaire possédant les clés "distance" (longueur de l'itinéraire)
                                               "duree" (durée du trajet)
                                               "geojson" (représentation de l'itinéraire au format GeoJSON)
    """
    reponse = requests.get(f"https://wxs.ign.fr/calcul/geoportail/itineraire/rest/1.0.0/route?resource=bdtopo-osrm&start={dep[1]}%2C{dep[0]}&end={arr[1]}%2C{arr[0]}&profile=car&optimization=fastest&constraints=%7B%22constraintType%22%3A%22banned%22%2C%22key%22%3A%22wayType%22%2C%22operator%22%3A%22%3D%22%2C%22value%22%3A%22autoroute%22%7D&getSteps=true&getBbox=true&distanceUnit=kilometer&timeUnit=hour&crs=EPSG%3A4326")
    reponse = reponse.json()
    distance = round(float(reponse["distance"]))
    duree = round(float(reponse["duration"]))
    geojson = reponse["geometry"]
    return {"distance" : distance, "duree" : duree, "geojson" : geojson}
  
def creer_carte():
    """
    Crée une carte folium centrée sur le centre de l'Hexagone (point de coordonnées (46.513°N ; 2.576°E))
    avec un niveau de zoom égal à 6.
    - Sortie : (variable contenant la carte)
    """
    return folium.Map(location=[46.513, 2.576], tiles="OpenStreetMap", zoom_start=6)
	
def enregistrer_carte(carte, nom_de_fichier):
    """
    Enregistre la carte dans un fichier HTML.
    - Entrées : carte (variable contenant une carte folium), nom_de_fichier (chaîne de caractères)
    - Effet de bord : enregistrement dans un fichier HTML
    """
    carte.save(f"{nom_de_fichier}.html")

def placer_marqueur(carte, lieu):
    """
    Place un marqueur sur la carte au lieu demandé.
    - Entrées : carte (variable contenant une carte folium),
                lieu (couple au format (adresse, code_postal), où adresse est une chaîne et code_postal un entier)
    - Sortie : carte (variable contenant une carte folium)
    """
    folium.Marker(_coord_BAN(lieu)).add_to(carte)
    return carte	
		
def tracer_itineraire(carte, depart, arrivee):
    """
    Représente sur la carte l'itinéaire le plus rapide entre depart et arrivee.
    - Entrées : carte (variable contenant une carte folium),
                depart, arrivee (couples au format (adresse, code_postal), où adresse est une chaîne et code_postal un entier)
    - Sortie : carte (variable contenant une carte folium)
    """
    carte = placer_marqueur(carte, depart)
    carte = placer_marqueur(carte, arrivee)
    geojson = _itineraire_IGN(_coord_BAN(depart), _coord_BAN(arrivee))["geojson"]
    folium.GeoJson(geojson).add_to(carte)
    return carte

def tracer_itineraire_multiple(carte, lieux):
    """
    Représente sur la carte l'itinéaire le plus rapide entre plusieurs lieux successifs.
    - Entrées : carte (variable contenant une carte folium),
                lieux (tableau contenant des couples au format (adresse, code_postal), où adresse est une chaîne et code_postal un entier)
    - Sortie : carte (variable contenant une carte folium)
    """
    for k in range(len(lieux)-1):
        carte = tracer_itineraire(carte, lieux[k], lieux[k+1])
    return carte

if __name__ == "__main__":
    depart = ("16 avenue Henri Mondor", 15000)
    intermediaire = ("24 avenue des Landais", 63170)
    arrivee = ("173 boulevard de Strasbourg", 94130)
    ma_carte = creer_carte()
    ma_carte = tracer_itineraire_multiple(ma_carte, [depart, intermediaire, arrivee])
    enregistrer_carte(ma_carte, "exemple")
