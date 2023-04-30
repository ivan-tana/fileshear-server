from app.extensions import database
from app.folder.folder import Folder as Folder_Class
from pathlib import Path
from .Collection import Collection
import pickle
import os


class Folder(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    path = database.Column(database.Text)
    collection_id = database.Column(
        database.Integer, database.ForeignKey("collection.id")
    )

    @property
    def allowed_extensions(self):
        return Collection.query.get(self.collection_id).allowed_extensions

    @property
    def data(self):

        try:

            folder_instance = get_folder_pickle(self.id)
            if folder_instance.last_mTime != os.stat(self.path).st_mtime:
                raise FileNotFoundError
        except FileNotFoundError:
            folder_instance = Folder_Class(Path(self.path), self.id, self.allowed_extensions)
            pickle_folder(folder_instance, self.id)
        return folder_instance

    @property
    def name(self):
        return self.data.name

    @property
    def folders(self):
        return self.data.folders

    @property
    def files(self):
        return self.data.files

    @property
    def all_files(self):
        return self.data.all_files

    @property
    def dict(self):
        return {
            "name": self.name,
            "file_count": len(self.all_files),
            "files": [file.dict for file in self.files],
            "all_files": [file.dict for file in self.all_files],
            "folders": [folder_instance.dict for folder_instance in self.folders],
            "allowed_extension": self.allowed_extensions,
            "collection_id": self.collection_id,
            "id": self.id,
        }

    def get_file_by_uid(self, uid):
        return self.data.get_file_by_uid(uid)


def pickle_folder(folder_instance, folder_id) -> None:
    print("pickling " + folder_instance.name)
    with open(str(Path("./pickled_folders/", str(folder_id))) + ".pickle", mode="wb") as fs:
        pickle.dump(folder_instance, fs)


def get_folder_pickle(folder_id):
    with open(str(Path("./pickled_folders/", str(folder_id))) + ".pickle", mode="rb") as fs:
        return pickle.load(fs)
