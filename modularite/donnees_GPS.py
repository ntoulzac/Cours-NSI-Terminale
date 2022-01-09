from requests import get
from PIL import Image
from PIL.ExifTags import TAGS

def _triplet_vers_angle(triplet, direction):
	angle = triplet[0] + triplet[1]/60 + triplet[2]/3600
	if direction in 'SW':
		return -angle
	else:
		return angle

def extraire_donnees_GPS(emplacement_image, type_emplacement='local'):
	if type_emplacement == 'local':
		image = Image.open(emplacement_image)
	elif type_emplacement == 'url':
		image = Image.open(get(emplacement_image, stream=True).raw)
	else:
		raise ValueError('Le paramètre type_emplacement est à chosir parmi "local" et "url"')
	largeur, hauteur = image.size
	image.verify()
	exif = image._getexif()
	dico = {}
	for (cle, valeur) in exif.items():
		if TAGS.get(cle) == 'GPSInfo':
			dico = valeur
	latitude = round(float(_triplet_vers_angle(dico[2], dico[1])), 5) if 1 in dico and 2 in dico else None
	longitude = round(float(_triplet_vers_angle(dico[4], dico[3])), 5) if 3 in dico and 4 in dico else None
	altitude = round(float(dico[6]), 1) if 6 in dico else None
	orientation = round(dico[17]) if 16 in dico and 17 in dico and dico[16] == 'T' else None
	return {'lat' : latitude,
	        'long' : longitude,
	        'alt' : altitude,
	        'orient' : orientation,
	        'larg' : largeur,
	        'haut' : hauteur}
		
if __name__ == '__main__':
	for k in range(15):
		try:
			print(f'PHOTO {k}\n', extraire_donnees_GPS(f'images/EXIF/{k}.jpg'), '\n')
		except:
			print(f'Erreur sur la photo {k} !')
