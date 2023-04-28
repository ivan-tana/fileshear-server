from app.extensions import database
from app.const import FileType


class Collection(database.Model):

    id = database.Column(database.Integer, primary_key=True)
    password = database.Column(database.Text, default='12345')
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
