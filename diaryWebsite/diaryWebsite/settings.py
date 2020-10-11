from .settings_base import *

GOOGLE_MAP_API_KEY = "YOUR_API_KEY"
MAP_WIDGETS = {
    "GooglePointFieldWidget": (
        ("zoom", 15),
        ("mapCenterLocation", [48.595629, 8.235968]),
        ("markerFitZoom", 11),
        (
            "GooglePlaceAutocompleteOptions",
            {"componentRestrictions": {}},
        ),
    ),
    "GOOGLE_MAP_API_KEY": GOOGLE_MAP_API_KEY,
}
