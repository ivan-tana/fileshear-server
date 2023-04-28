from flask import Blueprint
from flask_restful import Api
from . import resources
from . import models


folder = Blueprint(
    name="folder",
    import_name=__name__,
    url_prefix="/api",
)

folder_api = Api(folder)

# register resources
folder_api.add_resource(resources.Folder, "/folder")
folder_api.add_resource(resources.SingleFolder, "/<folder_id>")
folder_api.add_resource(resources.Collection, "/")
