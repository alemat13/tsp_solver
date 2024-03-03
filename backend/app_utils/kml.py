# Code sans doute à revoir

def generate_kml(points):
    # Données à utiliser pour générer le KML (exemple)
    data = {
        'lines': [
            {
                'name': 'Line 1',
                'coordinates': points
            },
        ]
    }

    # Rendu du template avec les données
    kml_content = render_template('map.kml', data=data)
    # Définir le type de contenu comme application/vnd.google-earth.kml+xml
    # pour indiquer qu'il s'agit d'un fichier KML
    return Response(
        kml_content,
        mimetype='application/vnd.google-earth.kml+xml',
        headers={'Content-Disposition': 'attachment; filename=' + 'map.kml'}
    )