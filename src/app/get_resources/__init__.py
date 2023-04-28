from flask import Blueprint, send_from_directory
from pathlib import Path
from app.models.Folder import Folder

get_resources = Blueprint(
    name="get_resources",
    import_name=__name__,
    url_prefix="/get/resource",
    static_folder="static",
)

PATH_TO_ICONS = str(Path(get_resources.root_path + "\\static\\icons\\"))


@get_resources.route("/icons/<suffix>")
def icon(suffix):
    # get icon file
    return send_from_directory(PATH_TO_ICONS, f"{suffix}.ico")


@get_resources.route("/file/<folder_id>/<uid>")
def file(folder_id, uid):
    folder_instance: Folder = Folder.query.get(folder_id)
    if folder_instance:
        file_instance = folder_instance.get_file_by_uid(uid)
        if file_instance:
            return send_from_directory(file_instance.parent, file_instance.name)
    return "File Not Found", 404
