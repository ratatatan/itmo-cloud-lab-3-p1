def c_to_f(celsius: float) -> float:
    """Convert Celsius to Fahrenheit."""
    return celsius * 9.0 / 5.0 + 32.0


def f_to_c(fahrenheit: float) -> float:
    """Convert Fahrenheit to Celsius."""
    return (fahrenheit - 32.0) * 5.0 / 9.0


def format_weather(city: str, temp_c: float) -> str:
    """Return formatted weather string in both C and F."""
    temp_f = c_to_f(temp_c)
    return f"Weather in {city}: {temp_c:.1f} °C / {temp_f:.1f} °F"
