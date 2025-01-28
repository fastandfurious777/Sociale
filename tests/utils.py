import json

def load_coords(place: str , data_file: str ='tests/data.json') -> str:
    """Loads and returns coords from a data file

    Args:
        place (str): Name of place at which are coords stored in data file
        data_file (str, optional): Name of file where data is stored. Defaults to 'data.json'.
    Raises:
        ValueError: If the file is not valid JSON or place is not found
    """
    if not is_json(data_file):
        raise ValueError(f"{data_file} is not proper json")
    
    with open(data_file) as file:
        data: list[dict[str, str]] = json.load(file)["Coords"]

    for coords in data:
        if place in coords:
            return coords[place]
    else:
        raise ValueError(f"Coordinates for {place} not found.")

def is_json(file: str) -> bool:
    """Checks whether given file is json

    Args:
        file (str): Name of a given file

    Returns:
        bool: True if a file is json, false otherwise
    """
    return file.split(".")[-1].lower() == "json"