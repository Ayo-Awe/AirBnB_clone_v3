#!/usr/bin/python3
"""Defines a blueprint
for app views
"""
from api.v1.views import app_views
from models import storage, classes


@app_views.route("/status")
def status():
    return {"status": "OK"}


@app_views.route("/stats")
def stats():
    payload = {}
    clss = {"amenities": classes["Amenity"], "cities": classes["City"],
            "places": classes["Place"], "reviews": classes["Review"],
            "states": classes["State"], "users": classes["User"]}

    for name, cls in clss.items():
        if cls.__name__ != "BaseModel":
            payload[name] = storage.count(cls)

    return payload
