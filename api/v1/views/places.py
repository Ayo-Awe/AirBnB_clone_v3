#!/usr/bin/python3
"""Route handler for places endpoints.
The endpoints supported are CRUD"""

from api.v1.views import app_views
from models import storage, Place, City, User
from flask import jsonify, abort, request, Response


@app_views.route("/cities/<id>/places", methods=["GET"], strict_slashes=False)
def get_places_by_city(id):
    """Route handler for getting all cities
    """
    city = storage.get(City, id)
    if city is None:
        abort(404)

    places = list(map(lambda x: x.to_dict(), city.places))

    return jsonify(places)


@app_views.route("/places/<id>", methods=["GET"], strict_slashes=False)
def get_place(id):
    """Route handler for getting a single
    place by id"""
    place = storage.get(Place, id)

    if place is None:
        abort(404)

    return place.to_dict()


@app_views.route("/cities/<id>/places", methods=["POST"],
                 strict_slashes=False)
def create_place(id):
    """Route handler for create a place
    the payload is in the form of a JSON object"""

    city = storage.get(City, id)
    if city is None:
        abort(404)

    body = request.get_json(silent=True)
    if body is None:
        abort(Response(status=400, response="Not a JSON"))

    if body.get("name") is None:
        abort(Response(status=400, response="Missing name"))

    if body.get("user_id") is None:
        abort(Response(status=400, response="Missing user_id"))

    if storage.get(User, body.get("user_id")) is None:
        abort(404)

    place = Place(name=body["name"], city_id=id, user_id=body["user_id"])

    place.save()

    return place.to_dict(), 201


@app_views.route("/places/<id>", methods=["DELETE"], strict_slashes=False)
def delete_place(id):
    """Route handler for deleting a place by
    id"""
    place = storage.get(Place, id)

    if place is None:
        abort(404)

    storage.delete(place)
    storage.save()

    return {}


@app_views.route("/places/<id>", methods=["PUT"], strict_slashes=False)
def update_place(id):
    """Route handler for updating a place object
    """
    place = storage.get(Place, id)

    if place is None:
        abort(404)

    body = request.get_json(silent=True)
    if body is None:
        abort(Response(status=400, response="Not a JSON"))

    payload = ignore_fields(
        body, ["id", "created_at", "updated_at", "__class__",
               "city_id", "user_id"])

    for key, value in payload.items():
        place.__setattr__(key, value)

    place.save()

    return place.to_dict()


def ignore_fields(mydict, fields):
    """Returns a dictionary and returns a copy
    without the keys specified in the fields
    argument"""

    copy = mydict.copy()

    for key in mydict.keys():
        if (key in fields):
            del copy[key]

    return copy
