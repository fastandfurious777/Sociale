from rest_framework.exceptions import ValidationError
from shapely import Polygon

def validate_polygon(geojson: dict) -> Polygon:
    """Validates a GeoJSON object and returns a Shapely Polygon

    Before using this function, please familiarize yourself with 
    the GeoJSON format: https://geojson.org/geojson-spec.html#id4

    Args:
        geojson (dict):  A GeoJSON dictionary representing a Polygon

    Raises:
        ValidationError: If the geojson is not dictionary,
        lacks required fields or the coordinates are improperly structured

    Returns:
        Polygon: A Shapely Polygon object created from the validated coordinates
    """

    if not isinstance(geojson, dict):
           raise ValidationError({"detail": "GeoJSON must be a dictionary"})

    if "type" not in geojson or "coordinates" not in geojson:
            raise ValidationError({"detail": "GeoJSON must contain 'type' and 'coordinates' fields"})

    if geojson["type"] != "Polygon":
        raise ValidationError({"detail": f"Invalid type. Expected 'Polygon', but received '{geojson['type']}'"})
    
    coordinates = geojson["coordinates"]

    if not isinstance(coordinates, list) or not coordinates:
        raise ValidationError({"detail": "Coordinates must be a list of lists"})

    if not isinstance(coordinates[0], list) or not coordinates[0]:
        raise ValidationError({"detail": "Polygon must have at least one ring with coordinate pairs"})

    ring = coordinates[0]

    if len(ring)<4:
        raise ValidationError({"detail": f"Polygon must have at least 4 coordinate pairs"})
    
    for point in ring:
        if not isinstance(point, list) or len(point)!=2:
            raise ValidationError({"detail": "Each coordinate pair must be a list of two numbers [lon, lat]"})

    if ring[0] != ring[-1]:
        raise ValidationError({"detail": "Polygon is not closed properly"})
    
    try:
        return Polygon(ring)
    except ValueError as e:
        raise ValidationError({"detail": f"Error creating Polygon: {str(e)}"})
        