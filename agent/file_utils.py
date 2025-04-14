from pathlib import Path
import os

def createFile(path, content):
    print(f"Creating file {path} ")
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content)

def readFile(path):
    try:
        print(f"Reading  file {path} ")
        return Path(path).read_text()
    except FileNotFoundError:
        return None


def replaceFileContent(path, new_content):
    """
    Replace the entire content of a file with new content.

    Args:
        path (str): Path to the file.
        new_content (str): The new content to write into the file.

    Returns:
        str: Success or error message.
    """
    try:
        print(f"updating  file {path} ")
        file_path = Path(path)
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(new_content)
        return f"Replaced content in: {path}"
    except Exception as e:
        return f"Error replacing content in {path}: {str(e)}"


def listFilesRecursive(root="."):
    return [str(p) for p in Path(root).rglob("*") if p.is_file()]


def deleteFile(path):
    try:
        print(f"deleting file {path} ")
        os.remove(path)
        return f"Deleted file: {path}"
    except FileNotFoundError:
        return f"File not found: {path}"
    except Exception as e:
        return str(e)