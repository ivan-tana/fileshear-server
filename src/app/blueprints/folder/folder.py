from pathlib import Path
import os


class File:
    """A class that represents a file in the file system.

    Attributes:
        path: A Path object that contain
         the absolute or relative path of the file.
        name: A string that contain
         the name of the file, including the extension.
    """

    def __init__(self, path: Path) -> None:
        """Initializes a File object with the given path.

        Args:
            path: A Path object that contain
             the absolute or relative path of the file.
        """
        self.path = path
        self.name = self.path.name

    def __repr__(self) -> str:
        """Returns a string representation of the File object.

        Returns:
            A string that contain
             the name of the file, including the extension.
        """
        return self.path.name


class Folder:
    """A class that represents a folder in the file system.

    Attributes:
        path: A Path object that contain
         the absolute or relative path of the folder.
        folders: A list of Folder objects that contain
         the sub-folders of the folder.
        files: A list of File objects that contain
         the files in the folder.
        all_files: A list of File objects that contain
         all the files in the folder and its sub-folders.
        name: the folder name and suffix
    """

    def __init__(self, path: Path, allowed_extensions: list[str] = None) -> None:
        """Initializes a Folder object with the given path and optional allowed extensions.

        Args:
            path: A Path object that contain
             the absolute or relative path of the folder.
            allowed_extensions: A list of strings that contain
             the file extensions that are allowed in the folder and its sub-folders. If None, all extensions are allowed. Defaults to None.
        """
        self.path = path
        self.name = self.path.name
        self.folders = list_folders(self.path, allowed_extensions)
        self.files = list_files(self.path, allowed_extensions)
        self.all_files = all_folder_files(self)

    def __repr__(self):
        """Returns a string representation of the Folder object.

        Returns:
            A string that contain
             the name of the folder.
        """
        return self.path.name

    def __eq__(self, other):
        """Returns True if two Folder objects have the same path and name, False otherwise.

        Args:
            other: Another Folder object to compare with.

        Returns:
            A boolean value indicating whether the two Folder objects are equal.
        """
        return self.path == other.path and self.name == other.name

    def search(self, term) -> list[File]:
        """Searches for files in the folder and its sub-folders that match the given term.

        Args:
            term: A string that contain
             the term to search for.

        Returns:
            A list of File objects that match the term. The files are matched if the term is a substring, a prefix, or a suffix of their names (case-insensitive).
        """
        result = []
        for file in self.all_files:
            if (
                term.lower() in file.name.lower()
                or file.name.lower().startswith(term.lower())
                or file.name.lower().endswith(term.lower())
            ):
                result.append(file)
        return result


def list_folders(path: Path, allowed_extension: list[str]) -> list[Folder]:
    """Lists all the sub-folders of a given path and creates Folder objects for them.

    Args:
        path: A Path object that contain
         the absolute or relative path of the folder to list.
        allowed_extension: A list of strings that contain
         the file extensions that are allowed in the sub-folders.

    Returns:
        A list of Folder objects that represent the sub-folders of the given path.
    """

    folder_list = []
    for (
        path,
        folders,
        files,
    ) in os.walk(path):
        [
            folder_list.append({"name": folder_item, "path": path})
            for folder_item in folders
        ]

    return [
        Folder(Path(folder_path["path"], folder_path["name"]), allowed_extension)
        for folder_path in folder_list
    ]


def all_folder_files(folder_item: Folder) -> list[File]:
    """
    Returns a list of all the files in a given folder and its sub-folders.

    Parameters
    ----------
    folder_item : Folder
        The folder to search for files.

    Returns
    -------
    list[File]
        A list of all the files in the folder and its sub-folders.
    """
    files = folder_item.files.copy()  # make a copy to avoid modifying the original list

    for fol in folder_item.folders:
        files.extend(
            all_folder_files(fol)
        )  # use recursion to get files from sub-folders

    return files


def list_files(path: Path, allowed_extensions: list[str] = None) -> list[File]:
    """
    Returns a list of files in a given path that match the allowed extensions.

    Parameters
    ----------
    path : Path
        The path to search for files.
    allowed_extensions : list[str], optional
        A list of file extensions to filter by. If None, all files are returned. (default is None)

    Returns
    -------
    list[File]
        A list of files in the path that match the allowed extensions.

    Raises
    ------
    FileExistsError
        If the path does not exist.
    """
    file_list = []
    if not path.exists():
        raise FileExistsError

    for file in path.iterdir():  # use iterdir instead of listdir for better performance
        if file.is_file() and (
            allowed_extensions is None or file.suffix in allowed_extensions
        ):
            file_list.append(File(file))

    return file_list


folder = Folder(Path("E:/files/Pictures/Camera Roll"))

[print(file) for file in folder.all_files]
