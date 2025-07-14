"""Constants for Flatlib Natal integration."""

DOMAIN = "flatlib_natal"

# Planet display names
PLANETS = {
    "Sun": "Sun",
    "Moon": "Moon",
    "Mercury": "Mercury",
    "Venus": "Venus",
    "Mars": "Mars",
    "Jupiter": "Jupiter",
    "Saturn": "Saturn",
}

# Угловые точки (используем ключи, как в данных сервера)
ANGLES = {
    "Asc": "Ascendant",
    "MC": "Midheaven",
}

# Important aspects to track
ASPECTS = [
    "Sun_to_Moon",
    "Sun_to_Ascendant",
    "Moon_to_Venus",
    "Venus_to_Mars",
    "Jupiter_to_Saturn",
]

# Zodiac sign icons
ZODIAC_SIGNS = {
    "Aries": "mdi:zodiac-aries",
    "Taurus": "mdi:zodiac-taurus",
    "Gemini": "mdi:zodiac-gemini",
    "Cancer": "mdi:zodiac-cancer",
    "Leo": "mdi:zodiac-leo",
    "Virgo": "mdi:zodiac-virgo",
    "Libra": "mdi:zodiac-libra",
    "Scorpio": "mdi:zodiac-scorpio",
    "Sagittarius": "mdi:zodiac-sagittarius",
    "Capricorn": "mdi:zodiac-capricorn",
    "Aquarius": "mdi:zodiac-aquarius",
    "Pisces": "mdi:zodiac-pisces",
}

# Специальные объекты (ключи должны точно совпадать с данными сервера)
SPECIAL_OBJECTS = {
    "North Node": "North Node",
    "South Node": "South Node",
    "Syzygy": "Lilith",
    "Pars Fortuna": "Pars Fortuna",
}

# House numbers (1-12)
HOUSES = list(range(1, 13))