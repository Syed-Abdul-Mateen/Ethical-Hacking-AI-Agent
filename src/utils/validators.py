import os
import re
from urllib.parse import urlparse

def is_valid_url(url: str) -> bool:
    """
    Validates if a given string is a correctly formatted HTTP/HTTPS URL.

    Args:
        url (str): The URL to validate.

    Returns:
        bool: True if valid, False otherwise.
    """
    try:
        result = urlparse(url)
        return all([result.scheme in ['http', 'https'], result.netloc])
    except ValueError:
        return False

def is_valid_directory(path: str) -> bool:
    """
    Validates if a given path exists and is a directory.

    Args:
        path (str): The directory path.

    Returns:
        bool: True if valid directory, False otherwise.
    """
    return os.path.exists(path) and os.path.isdir(path)

def is_valid_file(path: str) -> bool:
    """
    Validates if a given path exists and is a file.

    Args:
        path (str): The file path.

    Returns:
        bool: True if valid file, False otherwise.
    """
    return os.path.exists(path) and os.path.isfile(path)

def sanitize_input(user_input: str) -> str:
    """
    Sanitizes user input to prevent basic command injection when passed to shell.
    Note: Always prefer passing arguments as lists to subprocess over shell=True.

    Args:
        user_input (str): The input to sanitize.

    Returns:
        str: Sanitized input string.
    """
    return re.sub(r'[;&|`$]', '', user_input)
