
def search_term(term: str, file_list: list) -> list:
    """Searches for files in the folder and its sub-folders that match the given term.

    Args:
        term: A string that contain
         the term to search for.
        file_list: list of files

    Returns:
        A list of File objects that match the term. The files are matched if the term is a substring, a prefix, or a suffix of their names (case-insensitive).
    """
    results = []
    for file in file_list:
        if (
                term.lower() in file.name.lower()
                or file.name.lower().startswith(term.lower())
                or file.name.lower().endswith(term.lower())
        ):
            results.append(file)
    return [result.dict for result in results]
