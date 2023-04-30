from flask_restful import Resource, reqparse
from flask import request
from pathlib import Path
from app.models.Folder import Folder as FolderM
from app.models.Collection import Collection as CollectionM
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
        folders = FolderM.query.all()

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


class Collections(Resource):
    def get(self):

        results = []
        collections = CollectionM.query.all()
        for collection_instance in collections:
            results.append(collection_instance.dict)
        return results

    def post(self):
        if not is_local():
            return {"message": "request not allowed"}, 500
        collection_parser = reqparse.RequestParser()
        collection_parser.add_argument(
            "name", required=True, help="name invalid", type=str
        )
        collection_parser.add_argument(
            "type", required=True, help="type invalid", type=int
        )
        collection_parser.add_argument(
            "thumbnail", required=False, help="thumbnail invalid", type=str
        )
        collection_parser.add_argument(
            "public", required=False, help="public invalid", type=bool
        )
        collection_parser.add_argument(
            "password", required=False, help="password invalid", type=str
        )

        args = collection_parser.parse_args()

        name = args["name"]
        file_type = args["type"]
        thumbnail = args["thumbnail"] or ''
        public = args["public"] or False
        password = args["password"] or DEFUALT_PASSWORD
        try:
            new_collection = CollectionM(
                name=name,
                type=FileType(file_type),
                thumbnail=thumbnail,
                public=public,
                password=password,
            )

            database.session.add(new_collection)
            database.session.commit()

            return {"message": "collection Created", "collection_id": new_collection.id}
        except:
            return {"message": "failed to create collection"}, 500


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
