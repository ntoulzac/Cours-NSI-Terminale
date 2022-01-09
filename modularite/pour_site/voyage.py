import requests
import geodaisy.converters as conv
import folium

def _coord_BAN(lieu):
    """
    Détermine les coordonnées d'un lieu à partir d'une adresse, via l'API *Base Adresse Nationale*.
    - Entrée : lieu (couple au format (adresse, code_postal) où adresse est une chaîne et code_postal un entier)
    - Sortie : couple au format (latitude, longitude) où latitude et longitude sont des flottants
    """
    adresse, code_postal = lieu[0], lieu[1]
    url = f"https://api-adresse.data.gouv.fr/search/?q={adresse}&postcode={code_postal}"
    reponse = requests.get(url)
    reponse = reponse.json()
    coord = reponse['features'][0]['geometry']['coordinates']
    return [coord[1], coord[0]]

def _itineraire_IGN(dep, arr):
    """
    Détermine l'itinéraire le plus court entre deux lieux, via l'API *Itinéraires* de l'IGN.
    - Entrée : dep, arr (couples au format (latitude, longitude) où latitude et longitude sont des flottants)
    - Sortie : dictionnaire possédant les clés 'distance' (longueur de l'itinéraire)
                                               'duree' (durée du trajet)
                                               `geojson` (représentation de l'itinéraire au format GeoJSON)
    """
    reponse = requests.get(f"http://wxs.ign.fr/choisirgeoportail/itineraire/rest/route.json?origin={dep[1]},{dep[0]}&destination={arr[1]},{arr[0]}&method=TIME&graphName=Voiture")
    reponse = reponse.json()
    distance = round(float(reponse['distanceMeters']))
    duree = round(float(reponse['durationSeconds']))
    geojson = conv.wkt_to_geojson(reponse['geometryWkt'])
    return {'distance' : distance, 'duree' : duree, 'geojson' : geojson}
  
def creer_carte():
    pass
	
def enregistrer_carte(carte, nom_de_fichier):
    pass

def placer_marqueur(carte, lieu):
    pass	
		
def tracer_itineraire(carte, depart, arrivee):
    pass

def tracer_itineraire_multiple(carte, lieux):
    pass

if __name__ == '__main__':
    depart = ('16 avenue Henri Mondor', 15000)
    intermediaire = ('24 avenue des Landais', 63170)
    arrivee = ('173 boulevard de Strasbourg', 94130)
    ma_carte = creer_carte()
    ma_carte = tracer_itineraire_multiple(ma_carte, [depart, intermediaire, arrivee])
    enregistrer_carte(ma_carte, 'exemple')
