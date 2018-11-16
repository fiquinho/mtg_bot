"""
Utility functions for files manipulation and validation.
"""

from pathlib import Path
from typing import List


def validate_input_file(file_path: str, file_types: List[str]=None) -> Path:
    """
    Check if the file in that path exists and raises and error if it doesn't.
    Can check for the file extension to see if it matches to the accepted data
    types. Raises an error if it doesn't.

    :param file_path: The file to check
    :param file_types: The accepted data extensions.
    :return:
    """
    
    validated_path = Path(file_path)

    if not validated_path.exists():
        raise FileNotFoundError("The file {} doesn't exists.".format(validated_path))

    if file_types is not None:
        file_extension = validated_path.suffix
        if file_extension not in file_types:
            raise ValueError("File {} should be one of {} file types. "
                             "Found {} instead.".format(validated_path, file_types, file_extension))

    return validated_path
