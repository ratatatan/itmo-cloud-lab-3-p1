from ..core import c_to_f, f_to_c, format_weather


def test_c_to_f_and_back():
    c = 0.0
    f = c_to_f(c)
    assert abs(f - 32.0) < 1e-6
    c_back = f_to_c(f)
    assert abs(c_back - c) < 1e-6


def test_format_weather_contains_city_and_values():
    msg = format_weather("Moscow", 20.0)
    assert "Moscow" in msg
    assert "20.0" in msg
    assert "°C" in msg
    assert "°F" in msg
