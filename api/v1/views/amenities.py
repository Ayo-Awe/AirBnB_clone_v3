#!/usr/bin/python3
"""Route handler for amenities endpoints.
The endpoints supported are CRUD"""

from api.v1.views import app_views
from models import storage, Amenity
from flask import jsonify, abort, request, Response


@app_views.route("/amenities", methods=["GET"], strict_slashes=False)
def get_all_amenities():
    """Route handler for getting all amenities
    """
    amenities = storage.all(Amenity).values()
    amenities = list(map(lambda x: x.to_dict(), amenities))

    return jsonify(amenities)


@app_views.route("/amenities/<id>", methods=["GET"], strict_slashes=False)
def get_amenity(id):
    """Route handler for getting a single
    amenity by id"""
    amenity = storage.get(Amenity, id)

    if amenity is None:
        abort(404)

    return amenity.to_dict()


@app_views.route("/amenities", methods=["POST"], strict_slashes=False)
def create_amenity():
    """Route handler for create an amenity
    the payload is in the form of a JSON object"""
    body = request.get_json(silent=True)

    if body is None:
        abort(Response(status=400, response="Not a JSON"))

    if body.get("name") is None:
        abort(Response(status=400, response="Missing name"))

    amenity = Amenity(name=body["name"])
    amenity.save()

    return amenity.to_dict(), 201


@app_views.route("/amenities/<id>", methods=["DELETE"], strict_slashes=False)
def delete_amenity(id):
    """Route handler for deleting an amenity by
    id"""
    amenity = storage.get(Amenity, id)

    if amenity is None:
        abort(404)

    storage.delete(amenity)
    storage.save()

    return {}


@app_views.route("/amenities/<id>", methods=["PUT"], strict_slashes=False)
def update_amenity(id):
    """Route handler for updating a amenity object
    """
    amenity = storage.get(Amenity, id)

    if amenity is None:
        abort(404)

    body = request.get_json(silent=True)
    if body is None:
        abort(Response(status=400, response="Not a JSON"))

    payload = ignore_fields(
        body, ["id", "created_at", "updated_at", "__class__"])

    for key, value in payload.items():
        amenity.__setattr__(key, value)

    amenity.save()

    return amenity.to_dict()


def ignore_fields(mydict, fields):
    """Returns a dictionary and returns a copy
    without the keys specified in the fields
    argument"""

    copy = mydict.copy()

    for key in mydict.keys():
        if (key in fields):
            del copy[key]

    return copy
