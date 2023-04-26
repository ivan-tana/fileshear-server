[![Makefile CI](https://github.com/ivan-tana/fileshear-server/actions/workflows/makefile.yml/badge.svg)](https://github.com/ivan-tana/fileshear-server/actions/workflows/makefile.yml)

# fileshear-server

##Folder API Resource
This is an API resource class that handles the creation and retrieval of folders in the database. It has two methods: post and get.

##post
This method creates a new folder in the database and returns the names of the files in it.

### Parameters
- path: a string argument that specifies the path of the folder to be created
### Returns
a dictionary with a key ‘path’ and a value that is a list of file names in the folder
##get
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