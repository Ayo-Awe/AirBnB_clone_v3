#!/usr/bin/python3
"""Defines a blueprint
for app views
"""
from api.v1.views import app_views


@app_views.route("/status")
def status():
    return {"status": "OK"}
