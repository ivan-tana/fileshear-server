from app.extensions import database
from app.folder.folder import Folder as Folder_Class
from pathlib import Path


class Folder(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    path = database.Column(database.Text)
    collection_id = database.Column(database.Integer, database.ForeignKey('collection.id'))

    @property
    def data(self):
        return Folder_Class(Path(self.path))

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
    def allowed_extensions(self):
        return  self.data.allowed_extensions

    @property
    def dict(self):
        return {
            "name": self.name,
            "files": [file.dict for file in self.files],
            "all_files": [file.dict for file in self.all_files],
            "folders": [folder_instance.dict for folder_instance in self.folders],
            "allowed_extension": self.allowed_extensions
        }

    def get_file_by_uid(self, uid):
        return self.data.get_file_by_uid(uid)

