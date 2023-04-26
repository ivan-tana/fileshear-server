from src.app.extensions import database
from src.app.folder.folder import Folder as Folder_Class
from pathlib import Path


class Folder(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    path = database.Column(database.Text)

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

