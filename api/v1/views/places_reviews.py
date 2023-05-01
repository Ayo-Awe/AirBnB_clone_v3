#!/usr/bin/python3
"""Route handler for reviews endpoints.
The endpoints supported are CRUD"""

from api.v1.views import app_views
from models import storage, Review, Place, User
from flask import jsonify, abort, request, Response


@app_views.route("/places/<id>/reviews", methods=["GET"], strict_slashes=False)
def get_reviews_by_place(id):
    """Route handler for getting all reviews per place
    """
    place = storage.get(Place, id)
    if place is None:
        abort(404)

    reviews = list(map(lambda x: x.to_dict(), place.reviews))

    return jsonify(reviews)


@app_views.route("/reviews/<id>", methods=["GET"], strict_slashes=False)
def get_review(id):
    """Route handler for getting a single
    review by id"""
    review = storage.get(Review, id)

    if review is None:
        abort(404)

    return review.to_dict()


@app_views.route("/places/<id>/reviews", methods=["POST"],
                 strict_slashes=False)
def create_review(id):
    """Route handler for create a review
    the payload is in the form of a JSON object"""

    place = storage.get(Place, id)
    if place is None:
        abort(404)

    body = request.get_json(silent=True)
    if body is None:
        abort(Response(status=400, response="Not a JSON"))

    if body.get("text") is None:
        abort(Response(status=400, response="Missing text"))

    if body.get("user_id") is None:
        abort(Response(status=400, response="Missing user_id"))

    if storage.get(User, body.get("user_id")) is None:
        abort(404)

    review = Review(text=body["text"], place_id=id, user_id=body["user_id"])

    review.save()

    return review.to_dict(), 201


@app_views.route("/reviews/<id>", methods=["DELETE"], strict_slashes=False)
def delete_review(id):
    """Route handler for deleting a review by
    id"""
    review = storage.get(Review, id)

    if review is None:
        abort(404)

    storage.delete(review)
    storage.save()

    return {}


@app_views.route("/reviews/<id>", methods=["PUT"], strict_slashes=False)
def update_review(id):
    """Route handler for updating a review object
    """
    review = storage.get(Review, id)

    if review is None:
        abort(404)

    body = request.get_json(silent=True)
    if body is None:
        abort(Response(status=400, response="Not a JSON"))

    payload = ignore_fields(
        body, ["id", "created_at", "updated_at", "__class__",
               "place_id", "user_id"])

    for key, value in payload.items():
        review.__setattr__(key, value)

    review.save()

    return review.to_dict()


def ignore_fields(mydict, fields):
    """Returns a dictionary and returns a copy
    without the keys specified in the fields
    argument"""

    copy = mydict.copy()

    for key in mydict.keys():
        if (key in fields):
            del copy[key]

    return copy
