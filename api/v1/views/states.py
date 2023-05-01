#!/usr/bin/python3
"""Route handler for states endpoints.
The endpoints supported are CRUD"""

from api.v1.views import app_views
from models import storage, State
from flask import jsonify, abort, request, Response


@app_views.route("/states", methods=["GET"], strict_slashes=False)
def get_all_states():
    """Route handler for getting all states
    """
    states = storage.all(State).values()
    states = list(map(lambda x: x.to_dict(), states))

    return jsonify(states)


@app_views.route("/states/<id>", methods=["GET"], strict_slashes=False)
def get_state(id):
    """Route handler for getting a single
    state by id"""
    key = "{}.{}".format(State.__name__, id)
    states = storage.all(State)

    state = states.get(key)
    if state is None:
        abort(404)

    return state.to_dict()


@app_views.route("/states", methods=["POST"], strict_slashes=False)
def create_state():
    """Route handler for create a state
    the payload my be in the form of a JSON object"""
    body = request.get_json(silent=True)

    if body is None:
        abort(Response(status=400, response="Not a JSON"))

    if body.get("name") is None:
        abort(Response(status=400, response="Missing name"))

    state = State(name=body["name"])
    state.save()

    return state.to_dict(), 201


@app_views.route("/states/<id>", methods=["DELETE"], strict_slashes=False)
def delete_state(id):
    """Route handler for deleting a state by
    id"""
    key = "{}.{}".format(State.__name__, id)
    states = storage.all(State)

    state = states.get(key)
    if state is None:
        abort(404)

    storage.delete(state)
    storage.save()

    return {}


@app_views.route("/states/<id>", methods=["PUT"], strict_slashes=False)
def update_state(id):
    """Route handler for updating a state object
    """
    key = "{}.{}".format(State.__name__, id)
    states = storage.all(State)

    state = states.get(key)
    if state is None:
        abort(404)

    body = request.get_json(silent=True)
    if body is None:
        abort(Response(status=400, response="Not a JSON"))

    payload = ignore_fields(
        body, ["id", "created_at", "updated_at", "__class__"])

    for key, value in payload.items():
        state.__setattr__(key, value)

    state.save()

    return state.to_dict()


def ignore_fields(mydict, fields):
    """Returns a dictionary and returns a copy
    without the keys specified in the fields
    argument"""

    copy = mydict.copy()

    for key in mydict.keys():
        if (key in fields):
            del copy[key]

    return copy
