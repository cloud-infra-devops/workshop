from math import radians, sin, cos, sqrt, atan2
from mcp.server.fastmcp import FastMCP
from geopy.geocoders import Nominatim as GeoNominatim
import pgeocode

# Create server with stateless HTTP (required for AgentCore)
mcp = FastMCP(host="0.0.0.0", stateless_http=True)

_pgeo = pgeocode.Nominatim("us")
_geo = GeoNominatim(user_agent="zipcode_distance_mcp")


def _haversine(lat1, lon1, lat2, lon2) -> float:
    R = 6371.0
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlat, dlon = lat2 - lat1, lon2 - lon1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    return R * 2 * atan2(sqrt(a), sqrt(1 - a))


def _resolve(location: str) -> tuple[float, float, str]:
    """
    Resolve a location string (5-digit zip or city name) to (lat, lon, label).
    Raises ValueError if not found or outside the USA.
    """
    if location.strip().isdigit() and len(location.strip()) == 5:
        row = _pgeo.query_postal_code(location.strip())
        if row is None or row.latitude != row.latitude:
            raise ValueError(f"Zip code '{location}' not found.")
        return row.latitude, row.longitude, f"{location} ({row.place_name}, {row.state_code})"

    # City lookup — restrict to USA
    query = location if "," in location else f"{location}, USA"
    result = _geo.geocode(query, country_codes="us")
    if result is None:
        raise ValueError(f"City '{location}' not found in the USA.")
    return result.latitude, result.longitude, result.address


@mcp.tool()
def distance(location1: str, location2: str) -> str:
    """
    Calculate the distance between two US locations.

    Args:
        location1: A US city name (e.g. 'Chicago, IL') or 5-digit zip code (e.g. '10001')
        location2: A US city name (e.g. 'Los Angeles, CA') or 5-digit zip code (e.g. '90210')

    Returns:
        Distance in both miles and kilometers.
    """
    try:
        lat1, lon1, label1 = _resolve(location1)
        lat2, lon2, label2 = _resolve(location2)
    except ValueError as e:
        return str(e)

    km = _haversine(lat1, lon1, lat2, lon2)
    miles = km / 1.609344

    return (
        f"{label1} → {label2}\n"
        f"Distance: {miles:.2f} miles / {km:.2f} km"
    )


if __name__ == "__main__":
    mcp.run()
