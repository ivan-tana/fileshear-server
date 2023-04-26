from flask_restful import Resource, reqparse
from pathlib import Path
from src.app.models.Folder import Folder as FolderM
from src.app.extensions import database


class Folder(Resource):
    def get(self):
        return {"message": "Folder"}

    def post(self):
        folder_pars = reqparse.RequestParser()
        folder_pars.add_argument('path')
        args = folder_pars.parse_args()

        path = Path(args['path'])
        if path.exists():
            new_folder = FolderM(path=str(path))
            database.session.add(new_folder)
            database.session.commit()

            return {
                'path': [file.name for file in new_folder.all_files]
            }
