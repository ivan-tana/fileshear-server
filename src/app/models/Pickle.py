from app.extensions import database


class Binary(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    data = database.Column(database.LargeBinary)
    folder_id = database.Column(
        database.Integer, database.ForeignKey("folder.id")
    )