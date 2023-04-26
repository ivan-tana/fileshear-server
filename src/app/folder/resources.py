from flask_restful import Resource


class Folder(Resource):
    def get(self):
        return {"message": "Folder"}
