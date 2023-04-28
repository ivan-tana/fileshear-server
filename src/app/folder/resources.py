from flask_restful import Resource, reqparse
from pathlib import Path
from app.models.Folder import Folder as FolderM
from app.extensions import database


class Folder(Resource):
    def get(self):
        """
        This method queries all the folders in the database and returns a dictionary with their information.

        Parameters:
        - self: the instance of the class that calls this method

        Returns:
        - a dictionary with two keys: 'count' and 'folders'
        - 'count' is an integer that represents the number of folders in the database
        - 'folders' is a list of dictionaries, each containing the attributes of a folder instance
        - a folder instance has the following attributes:
            - 'name': a string that is the name of the folder
            - 'files': a list of dictionaries, each containing the attributes of a file instance that belongs to the folder
            - 'all_files': a list of dictionaries, each containing the attributes of a file instance that belongs to the folder or any of its subfolders
            - 'folders': a list of dictionaries, each containing the attributes of a subfolder instance that belongs to the folder
            - 'allowed_extension': a list of strings that are the allowed file extensions for the folder
        """
        # query all the folders in the database
        folders = FolderM.query.all()

        context = {
            "count": len(folders),
            "folders": [folder_instance.dict for folder_instance in folders]
        }
        return context

    def post(self):
        """
        This method creates a new folder in the database and returns the names of the files in it.

        Parameters:
        - self: the instance of the class that calls this method
        - path: a string argument that specifies the path of the folder to be created

        Returns:
        - a dictionary with a key 'path' and a value that is a list of file names in the folder
        """
        # create a parser object to parse the path argument
        folder_pars = reqparse.RequestParser()
        folder_pars.add_argument('path')
        args = folder_pars.parse_args()

        # convert the path argument to a Path object
        path = Path(args['path'])
        # check if the path exists
        if path.exists():
            # create a FolderM object with the path as an attribute
            new_folder = FolderM(path=str(path))
            # add the folder to the database session
            database.session.add(new_folder)
            # commit the changes to the database
            database.session.commit()

            # return a dictionary with the file names in the folder
            return {
                'message': "success"
            }
        return {
                   "message": "Failed to add folder"
               }, 400


class SingleFolder(Resource):
    def get(self, folder_id):
        folder = FolderM.query.get(folder_id)
        if folder:
            return folder.dict
        return {
            "message": "folder not found"
        }, 400

    def delete(self, folder_id):
        """
        delete folder
        """
        folder_instance = FolderM.query.get(folder_id)
        if folder_instance:
            database.session.delete(folder_instance)
            database.session.commit()
            return {
                "message": "folder deleted"
            }
        return {
            "message": "folder dose not exist"
        }


