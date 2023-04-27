from flask import Blueprint, send_from_directory
from pathlib import Path

get_resources = Blueprint(
    name="get_resources",
    import_name=__name__,
    url_prefix="/get/resource",
    static_folder='static'
)

PATH_TO_ICONS = str(Path(get_resources.root_path + "\\static\\icons\\"))


@get_resources.route('/icons/<suffix>')
def icon(suffix):
    # get icon file
    return send_from_directory(PATH_TO_ICONS, f'{suffix}.ico')
