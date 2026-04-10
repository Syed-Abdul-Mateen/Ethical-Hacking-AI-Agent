import os
import mimetypes
import logging
from typing import Optional

logger = logging.getLogger(__name__)

def read_file_safely(file_path: str, max_size_bytes: int = 10 * 1024 * 1024) -> Optional[str]:
    """
    Safely reads a file's content, checking for size limits and handling encoding errors.

    Args:
        file_path (str): The absolute or relative path to the file.
        max_size_bytes (int): Maximum allowed file size in bytes (default 10MB).

    Returns:
        Optional[str]: The file content as a string, or None if reading fails.
    """
    if not os.path.exists(file_path):
        logger.warning(f"File not found: {file_path}")
        return None

    try:
        if os.path.getsize(file_path) > max_size_bytes:
            logger.warning(f"File exceeds maximum size limit ({max_size_bytes} bytes): {file_path}")
            return None

        with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
            return f.read()
    except Exception as e:
        logger.error(f"Error reading file {file_path}: {e}")
        return None

def write_file_safely(file_path: str, content: str) -> bool:
    """
    Safely writes content to a file, ensuring the directory exists.

    Args:
        file_path (str): The path to the target file.
        content (str): The content to write.

    Returns:
        bool: True if successful, False otherwise.
    """
    try:
        os.makedirs(os.path.dirname(os.path.abspath(file_path)), exist_ok=True)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    except Exception as e:
        logger.error(f"Error writing to file {file_path}: {e}")
        return False

def get_mime_type(file_path: str) -> str:
    """
    Detects the MIME type of a file based on its extension.

    Args:
        file_path (str): The path to the file.

    Returns:
        str: The detected MIME type, or 'application/octet-stream' as a fallback.
    """
    mime_type, _ = mimetypes.guess_type(file_path)
    return mime_type or 'application/octet-stream'

def is_binary_file(file_path: str) -> bool:
    """
    Checks if a file is likely a binary file based on its MIME type.

    Args:
        file_path (str): The path to the file.

    Returns:
        bool: True if binary, False otherwise.
    """
    mime_type = get_mime_type(file_path)
    return not (mime_type.startswith('text/') or mime_type in ['application/json', 'application/javascript', 'application/xml'])
