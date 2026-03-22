from mcp.server.fastmcp import FastMCP

mcp = FastMCP("convert units from fps to mks measurement system")

# Conversion factors to MKS
CONVERSIONS = {
    "feet_to_meters":       ("length",   0.3048),
    "miles_to_meters":      ("length",   1609.344),
    "inches_to_meters":     ("length",   0.0254),
    "pounds_to_kilograms":  ("mass",     0.45359237),
    "ounces_to_kilograms":  ("mass",     0.02834952),
    "slugs_to_kilograms":   ("mass",     14.593903),
    "fps_to_mps":           ("velocity", 0.3048),       # feet/s → m/s
    "mph_to_mps":           ("velocity", 0.44704),      # miles/h → m/s
    "lbf_to_newtons":       ("force",    4.4482216),    # pound-force → N
    "psi_to_pascal":        ("pressure", 6894.757),     # lb/in² → Pa
    "btu_to_joules":        ("energy",   1055.056),
    "hp_to_watts":          ("power",    745.69987),
    "fahrenheit_to_celsius": ("temperature", None),     # special case
}


@mcp.tool()
def convert(value: float, unit: str) -> str:
    """
    Convert a value from FPS to MKS units.

    Args:
        value: Numeric value to convert
        unit:  Conversion key, e.g. 'feet_to_meters', 'pounds_to_kilograms',
               'fps_to_mps', 'lbf_to_newtons', 'psi_to_pascal', 'btu_to_joules',
               'hp_to_watts', 'fahrenheit_to_celsius'
    """
    if unit not in CONVERSIONS:
        available = ", ".join(CONVERSIONS.keys())
        return f"Unknown unit '{unit}'. Available: {available}"

    category, factor = CONVERSIONS[unit]

    if unit == "fahrenheit_to_celsius":
        result = (value - 32) * 5 / 9
        return f"{value} °F = {result:.6g} °C"

    result = value * factor
    return f"{value} ({unit.split('_to_')[0]}) = {result:.6g} ({unit.split('_to_')[1]}) [{category}]"


@mcp.tool()
def list_conversions() -> str:
    """List all supported FPS-to-MKS conversions."""
    lines = [f"  {k}  [{v[0]}]" for k, v in CONVERSIONS.items()]
    return "Supported conversions:\n" + "\n".join(lines)


if __name__ == "__main__":
    mcp.run()
