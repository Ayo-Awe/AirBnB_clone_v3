#!/usr/bin/python3
"""Route handler for cities endpoints.
The endpoints supported are CRUD"""

from api.v1.views import app_views
from models import storage, City, State
from flask import jsonify, abort, request, Response


@app_views.route("/states/<id>/cities", methods=["GET"], strict_slashes=False)
def get_cities_by_state(id):
    """Route handler for getting all states
    """
    state = storage.get(State, id)
    if state is None:
        abort(404)

    cities = list(map(lambda x: x.to_dict(), state.cities))

    return jsonify(cities)


@app_views.route("/cities/<id>", methods=["GET"], strict_slashes=False)
def get_city(id):
    """Route handler for getting a single
    city by id"""
    city = storage.get(City, id)

    if city is None:
        abort(404)

    return city.to_dict()


@app_views.route("/states/<id>/cities", methods=["POST"], strict_slashes=False)
def create_city(id):
    """Route handler for create a city
    the payload is in the form of a JSON object"""

    state = storage.get(State, id)
    if state is None:
        abort(404)

    body = request.get_json(silent=True)
    if body is None:
        abort(Response(status=400, response="Not a JSON"))

    if body.get("name") is None:
        abort(Response(status=400, response="Missing name"))

    city = City(name=body["name"], state_id=id)

    city.save()

    return city.to_dict(), 201


@app_views.route("/cities/<id>", methods=["DELETE"], strict_slashes=False)
def delete_city(id):
    """Route handler for deleting a city by
    id"""
    city = storage.get(City, id)

    if city is None:
        abort(404)

    storage.delete(city)
    storage.save()

    return {}


@app_views.route("/cities/<id>", methods=["PUT"], strict_slashes=False)
def update_city(id):
    """Route handler for updating a city object
    """
    city = storage.get(City, id)

    if city is None:
        abort(404)

    body = request.get_json(silent=True)
    if body is None:
        abort(Response(status=400, response="Not a JSON"))

    payload = ignore_fields(
        body, ["id", "created_at", "updated_at", "__class__", "state_id"])

    for key, value in payload.items():
        city.__setattr__(key, value)

    city.save()

    return city.to_dict()


def ignore_fields(mydict, fields):
    """Returns a dictionary and returns a copy
    without the keys specified in the fields
    argument"""

    copy = mydict.copy()

    for key in mydict.keys():
        if (key in fields):
            del copy[key]

    return copy
