from PIL import Image
from PIL.ExifTags import TAGS

def _triplet_vers_angle(triplet, direction):
	angle = triplet[0] + triplet[1]/60 + triplet[2]/3600
	if direction in 'SW':
		return -angle
	else:
		return angle

def extraire_donnees_GPS(nom_de_fichier):
	image = Image.open(nom_de_fichier)
	taille = image.size
	image.verify()
	exif = image._getexif()
	for (cle, valeur) in exif.items():
		if TAGS.get(cle) == 'GPSInfo':
			dico = valeur
	latitude = float(_triplet_vers_angle(dico[2], dico[1]))
	longitude = float(_triplet_vers_angle(dico[4], dico[3]))
	altitude = float(dico[6])
	orientation = round(dico[17]) if dico[16] == 'T' else None
	return {'lat' : round(latitude, 5),
			'long' : round(longitude, 5),
			'alt' : round(altitude, 1),
			'orient' : orientation,
			'largeur' : taille[0],
			'hauteur' : taille[1]}

if __name__ == '__main__':
	for k in range(1, 13):
		try:
			print(f'PHOTO {k}\n', extraire_donnees_GPS(f'images/EXIF/{k}.jpg'), '\n')
		except:
			print(f'Erreur sur la photo {k} !')
