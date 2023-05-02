from app.extensions import database
from importlib import import_module
from app.folder.folder import Folder as Folder_Class
from .Pickle import Binary
from pathlib import Path
from .Collection import Collection
import pickle
import os


class Folder(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    path = database.Column(database.Text)
    pickle_data = database.relationship("Binary", cascade="all,delete", backref="folder", lazy=True)
    collection_id = database.Column(
        database.Integer, database.ForeignKey("collection.id")
    )


    @property
    def exist(self):
        return Path(self.path).exists()

    @property
    def existing_folders(self):
        results = []
        for folder in self.folders:
            if folder.exist:
                results.append(folder)
        return results

    @property
    def allowed_extensions(self):
        return Collection.query.get(self.collection_id).allowed_extensions

    @property
    def data(self):
        if self.exist:
            try:
                folder_instance = get_folder_pickle(self.id)
                print(folder_instance.name)
                if folder_instance.last_mTime != os.stat(self.path).st_mtime:
                    raise FileNotFoundError
            except:

                folder_instance = Folder_Class(Path(self.path), self.id, self.allowed_extensions)
                pickle_folder(folder_instance, self.id)
            return folder_instance
        else:
            return None

    @property
    def name(self):
        if self.data is not None:
            return self.data.name
        return ''

    @property
    def folders(self):
        if self.data is not None:
            return self.data.folders
        return ''

    @property
    def files(self):
        if self.data is not None:
            return self.data.files
        return ''

    @property
    def all_files(self):
        if self.data is not None:
            return self.data.all_files
        return ''

    @property
    def dict(self):
        return {
            "name": self.name,
            "exist": self.exist,
            "file_count": len(self.all_files),
            "files": [file.dict for file in self.files],
            "all_files": [file.dict for file in self.all_files],
            "folders": [folder_instance.dict for folder_instance in self.existing_folders],
            "allowed_extension": self.allowed_extensions,
            "collection_id": self.collection_id,
            "id": self.id,
        }

    def get_file_by_uid(self, uid):
        return self.data.get_file_by_uid(uid)


def pickle_folder(folder_instance, folder_id) -> None:
    pickle_instance = Binary(folder_id=folder_id, data=pickle.dumps(folder_instance))
    database.session.add(pickle_instance)
    database.session.commit()


def get_folder_pickle(folder_id):

    pickle_instance = Binary.query.get(folder_id)
    return pickle.loads(pickle_instance.data)
