#!/usr/bin/python3
"""Route handler for users endpoints.
The endpoints supported are CRUD"""

from api.v1.views import app_views
from models import storage, User
from flask import jsonify, abort, request, Response


@app_views.route("/users", methods=["GET"], strict_slashes=False)
def get_all_users():
    """Route handler for getting all users
    """
    users = storage.all(User).values()
    users = list(map(lambda x: x.to_dict(), users))

    return jsonify(users)


@app_views.route("/users/<id>", methods=["GET"], strict_slashes=False)
def get_user(id):
    """Route handler for getting a single
    user by id"""
    user = storage.get(User, id)

    if user is None:
        abort(404)

    return user.to_dict()


@app_views.route("/users", methods=["POST"], strict_slashes=False)
def create_user():
    """Route handler for create an user
    the payload is in the form of a JSON object"""
    body = request.get_json(silent=True)

    if body is None:
        abort(Response(status=400, response="Not a JSON"))

    if body.get("email") is None:
        abort(Response(status=400, response="Missing email"))

    if body.get("password") is None:
        abort(Response(status=400, response="Missing password"))

    user = User(email=body["email"], password=body["password"])
    user.save()

    return user.to_dict(), 201


@app_views.route("/users/<id>", methods=["DELETE"], strict_slashes=False)
def delete_user(id):
    """Route handler for deleting an user by
    id"""
    user = storage.get(User, id)

    if user is None:
        abort(404)

    storage.delete(user)
    storage.save()

    return {}


@app_views.route("/users/<id>", methods=["PUT"], strict_slashes=False)
def update_user(id):
    """Route handler for updating a user object
    """
    user = storage.get(User, id)

    if user is None:
        abort(404)

    body = request.get_json(silent=True)
    if body is None:
        abort(Response(status=400, response="Not a JSON"))

    payload = ignore_fields(
        body, ["id", "created_at", "updated_at", "__class__", "email"])

    for key, value in payload.items():
        user.__setattr__(key, value)

    user.save()

    return user.to_dict()


def ignore_fields(mydict, fields):
    """Returns a dictionary and returns a copy
    without the keys specified in the fields
    argument"""

    copy = mydict.copy()

    for key in mydict.keys():
        if (key in fields):
            del copy[key]

    return copy
