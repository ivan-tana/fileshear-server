from app.folder.folder import Folder, list_folders
import pytest
from app import create_app
from pathlib import Path
from typing import List


@pytest.fixture()
def app():
    app = create_app()
    app.config.update(
        {
            "TESTING": True,
        }
    )

    # other setup can go here

    yield app

    # clean up / reset resources here

@pytest.fixture()
def test_list_folders(app, tmpdir: Path):

# Create a temporary directory structure

    tmpdir.mkdir("folder1").join("file1.txt").write("content")
    tmpdir.mkdir("folder2").join("file2.txt").write("content")
    tmpdir.mkdir("folder3").join("file3.txt").write("content")

    # Define the allowed extensions
    allowed_extensions = [".txt"]

    # Call the list_folders function
    result = list_folders(tmpdir, allowed_extensions)

    # Assert that the result is as expected
    assert len(result) == 3
    assert all(isinstance(folder, Folder) for folder in result)
    assert all(
        folder.path.name in ["folder1", "folder2", "folder3"] for folder in result
    )
