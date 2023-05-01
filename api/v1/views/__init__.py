from flask import Blueprint

app_views = Blueprint(name="app_views", url_prefix="/api/v1", import_name=__name__)
from api.v1.views.index import *
from api.v1.views.states import *
from api.v1.views.cities import *
