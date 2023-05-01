[![Makefile CI](https://github.com/ivan-tana/fileshear-server/actions/workflows/makefile.yml/badge.svg)](https://github.com/ivan-tana/fileshear-server/actions/workflows/makefile.yml)

# FileShear Rest Api

## Rest api routes

The following are the various routes available in the api, their functions and how to use them

## create a new collection
send a post request to `/api/collection`

**Example**: To create a collection an image collection called art 
```json
{
    "name": "art",
    "type":2,
    "public": false,
    "password": "1234567809",
    "thumbnail": "E:videos/thumbnail.png"
}
```

The `name` and `type` are required when creating a new collection the others can be left out
```json
{
  "name": "art",
  "type": 2
}
```
if the creation is successful 
```json
{"message": "collection Created", "collection_id": 1}
```
the response status code will be 500 and the responce json
```json
{"message": "failed to create collection"} 
```

**Note**: post, get and delete request can only be sent with localhost ip

## view collection
Send a get request to `/api/collection` to get a list of the collections available

**Example**: 

```json
[
    {
        "id": 1,
        "type": 2,
        "public": false,
        "name": "art",
        "thumbnail": "E:videos/thumbnail.png",
        "folders": []
    }
]

```

view a spacific collection by sending a get request to `/api/collection/<collection_id>` eg `/api/collection/1`

## Delete collection
send a delete request to `api/collection/<collection_id>`

## Folder API Resource
This is an API resource class that handles the creation and retrieval of folders in the database. It has two methods: post and get.

## post
This method creates a new folder in the database and returns the names of the files in it.

### Parameters
- path: a string argument that specifies the path of the folder to be created
### Returns
a success message if the folder was added amd failed if not
## get
This method queries all the folders in the database and returns a dictionary with their information.

Parameters
- none
## Returns
a dictionary with two keys: ‘count’ and ‘folders’

- ‘count’ is an integer that represents the number of folders in the database
  - ‘folders’ is a list of dictionaries, each containing the attributes of a folder instance
  a folder instance has the following attributes:
  - ‘name’: a string that is the name of the folder
  - ‘files’: a list of dictionaries, each containing the attributes of a file instance that belongs to the folder
  - ‘all_files’: a list of dictionaries, each containing the attributes of a file instance that belongs to the folder or any of its subfolders
  - ‘folders’: a list of dictionaries, each containing the attributes of a subfolder instance that belongs to the folder
  - ‘allowed_extension’: a list of strings that are the allowed file extensions for the folder

pyinstaller  --add-data "app/get_resources/static;app\get_resources\static" --add-data "app\config_flask_app.py;app\config_flask_app.py" --onefile app.py