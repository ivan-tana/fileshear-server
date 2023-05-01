from flask_restful import Resource, reqparse
from flask import request
from pathlib import Path
from app.models.Folder import Folder as FolderM
from app.models.Collection import Collection as CollectionM
from app.functions import get_existing_folders
from app.extensions import database
from app.const import FileType, DEFUALT_PASSWORD


def is_local():
    return "localhost" in str(request.root_url) or "127.0.0" in str(request.root_url)


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
        folders = get_existing_folders(FolderM)

        context = {
            "count": len(folders),
            "folders": [folder_instance.dict for folder_instance in folders],
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
        if not is_local():
            return {"message": "request not allowed"}, 500
        # create a parser object to parse the path argument
        folder_pars = reqparse.RequestParser()
        folder_pars.add_argument("path", required=True, help="path invalid")
        folder_pars.add_argument("collection_id", required=True, help="collection_id invalid")
        args = folder_pars.parse_args()

        # convert the path argument to a Path object
        path = Path(args["path"])
        collection = CollectionM.query.get(args["collection_id"])
        # check if the path exists
        if path.exists() and collection:
            # create a FolderM object with the path as an attribute
            new_folder = FolderM(path=str(path), collection_id=collection.id)
            # add the folder to the database session
            database.session.add(new_folder)
            # commit the changes to the database
            database.session.commit()

            # return a dictionary with the file names in the folder
            return {"message": "success"}
        return {"message": "Failed to add folder"}, 400


class SingleFolder(Resource):
    def get(self, folder_id):
        folder = FolderM.query.get(folder_id)
        if folder:
            return folder.dict
        return {"message": "folder not found"}, 400

    def delete(self, folder_id):
        if not is_local():
            return {"message": "request not allowed"}, 500
        """
        delete folder
        """
        folder_instance = FolderM.query.get(folder_id)
        if folder_instance:
            database.session.delete(folder_instance)
            database.session.commit()
            return {"message": "folder deleted"}
        return {"message": "folder dose not exist"}, 404


# This class defines a resource for collections
class Collections(Resource):
    # This method returns a list of all collections in the database
    def get(self):

        results = []  # Initialize an empty list to store the results
        collections = CollectionM.query.all()  # Query all collections from the database
        for collection_instance in collections:  # Loop through each collection
            results.append(
                collection_instance.dict)  # Append the dictionary representation of the collection to the results list
        return results  # Return the results list

    # This method creates a new collection in the database
    def post(self):
        if not is_local():  # Check if the request is local
            return {"message": "request not allowed"}, 500  # If not, return an error message and status code 500
        collection_parser = reqparse.RequestParser()  # Create a parser object to parse the request arguments
        collection_parser.add_argument(
            "name", required=True, help="name invalid", type=str
        )  # Add an argument for the name of the collection, which is required and must be a string
        collection_parser.add_argument(
            "type", required=True, help="type invalid", type=int
        )  # Add an argument for the type of the collection, which is required and must be an integer
        collection_parser.add_argument(
            "thumbnail", required=False, help="thumbnail invalid", type=str
        )  # Add an argument for the thumbnail of the collection, which is optional and must be a string
        collection_parser.add_argument(
            "public", required=False, help="public invalid", type=bool
        )  # Add an argument for the public status of the collection, which is optional and must be a boolean
        collection_parser.add_argument(
            "password", required=False, help="password invalid", type=str
        )  # Add an argument for the password of the collection, which is optional and must be a string

        args = collection_parser.parse_args()  # Parse the arguments from the request

        name = args["name"]  # Get the name from the arguments
        file_type = args["type"]  # Get the type from the arguments
        thumbnail = args["thumbnail"] or ''  # Get the thumbnail from the arguments or use an empty string as default
        public = args["public"] or False  # Get the public status from the arguments or use False as default
        password = args[
                       "password"] or DEFUALT_PASSWORD  # Get the password from the arguments or use a default password as defined in a constant

        try:
            new_collection = CollectionM(
                name=name,
                type=FileType(file_type),
                thumbnail=thumbnail,
                public=public,
                password=password,
            )  # Create a new collection object with the given attributes

            database.session.add(new_collection)  # Add the new collection to the database session
            database.session.commit()  # Commit the changes to the database

            return {"message": "collection Created",
                    "collection_id": new_collection.id}  # Return a success message and the id of the new collection
        except:
            return {
                       "message": "failed to create collection"}, 500  # If an exception occurs, return an error message and status code 500


class SearchCollections(Resource):
    def get(self, term):
        collections = CollectionM.query.all()
        results = []
        for collection_instance in collections:
            results += collection_instance.search(term)
        return results


class SearchCollection(Resource):
    def get(self, collection_id, term):
        collection_query = CollectionM.query.get(collection_id)
        if collection_query:
            return collection_query.search(term)
        return []


class Collection(Resource):
    def get(self, collection_id):
        collection_instance = CollectionM.query.get(collection_id)
        if collection_instance:
            return collection_instance.dict
        return {"massage": "collection not found"}, 404

    def delete(self, collection_id):
        if not is_local():
            return {"message": "request not allowed"}, 500
        collection_instance = CollectionM.query.get(collection_id)
        database.session.delete(collection_instance)
        database.session.commit()
        return {
            "message": "collection deleted",
        }


class Summary(Resource):
    def get(self):
        collections = CollectionM.query.all()
        folders = FolderM.query.all()

        return {
            "collection_count": len(collections),
            "folder_count": len(folders),
            "collections": [collection.name for collection in collections],
            "collection_types": [{collection.name: collection.type.value} for collection in collections]
        }
