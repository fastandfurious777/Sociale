from datetime import datetime
import re
from rest_framework.exceptions import ValidationError # type: ignore
from base.models import Parking
from typing import Iterable

def date_validate(date: str | datetime) -> datetime:
    """Validates and parses a string or datetime into a datetime object

    Args:
        date (str | datetime): String formatted as 'yyyy-mm-dd hh:mm:ss' or a datetime object

    Raises:
        ValidationError: If the string is not formatted properly

    Returns:
        datetime: A validated datetime object
    """
    if isinstance(date, datetime):
        return date
    if re.fullmatch(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}', str(date)) is not None:
        format_data: str = "%Y-%m-%d %H:%M:%S"
        return datetime.strptime(date, format_data)
    else:
        raise ValidationError("Date must be a string formatted as 'yyyy-mm-dd hh:mm:ss'")
    
def parking_location_validate(lon: float, lat: float, parkings: Iterable[Parking]) -> bool:
    """Checks if a given location is within parking spots

    Args:
        lon (int): Longtitude of location
        lat (int): Latitude of location
        parkings (Iterable[Parking]): List of parking spots 

    Returns:
        bool: True if location is within any parking spot, False otherwise
    """
    for parking in parkings:
        if parking.contains_point(lon=lon,lat=lat):
            return True
    return False
    