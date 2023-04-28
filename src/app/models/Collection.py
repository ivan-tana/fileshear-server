from app.extensions import database
from app.const import FileType, DEFUALT_PASSWORD
from app.functions import search_term
from app.exceptions import InvalidPassword

class Collection(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    password = database.Column(database.Text, default=DEFUALT_PASSWORD)
    thumbnail = database.Column(database.Text)
    name = database.Column(database.String(30), nullable=False)
    type = database.Column(database.Enum(FileType), nullable=False)
    public = database.Column(database.Boolean(), default=False)
    folders = database.relationship('Folder', backref='collection', lazy=True)

    @property
    def all_files(self):
        files = []
        for folder_instance in self.folders:
            files.append(folder_instance.all_files)
        return files

    def search(self, term: str) -> list:
        return search_term(term, self.all_files)

    @property
    def dict(self):
        return {
            "type": self.type.value,
            "public": self.public,
            "name": self.name,
            "thumbnail": self.thumbnail,
            "folders": [folder_instance.dict for folder_instance in self.folders],
        }

    def change_password(self, current_password: str, new_password: str):
        if current_password == self.password:
            self.password = new_password
            return
        raise InvalidPassword("The current password is invalid")

    def toggle_access_type(self):
        """toggle access type"""
        self.public = not self.public

    def update_thumbnail(self, thumbnail: str):
        """update thumbnail"""
        self.thumbnail = thumbnail

