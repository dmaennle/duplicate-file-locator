from pathlib import Path
from typing import Callable
from joblib import Parallel, delayed

def compute_sha256_hash(file_path: Path) -> tuple:
    """
    Compute the SHA256 hash of a file.

    Parameters:
    -----------
    file_path: Path
        The path to the file.

    Returns:
    --------
    tuple of str and Path
    """
    import hashlib
    hash_obj = hashlib.sha256()
    with file_path.open("rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            hash_obj.update(chunk)
    return (hash_obj.hexdigest(), file_path)


class DuplicateFileLocator:
    """
    A class to locate duplicate files in a directory.

    It will use the file size to first identify potential duplicates and then
    compare the content of the files to confirm if they are duplicates.

    It will use the provided hashing algorithm to compare the content of the
    files. Default hashing algorithm is SHA256.

    Attributes:
    -----------
    hash_funct: callable
        A callable that takes a file path and returns the hash of the file.
        Default is filedup.compute_sha256_hash().
    """

    hash_funct: Callable

    def __init__(self,
                 hash_funct: Callable = compute_sha256_hash):
        self.hash_funct = hash_funct

    def _get_file_size(self, file_path: Path) -> tuple:
        """
        Get the size of a file.

        Parameters:
        -----------
        file_path: Path
            The path to the file.

        Returns:
        --------
        tuple of int and Path
        """
        return (file_path.stat().st_size, file_path)

    def find_duplicates(self,
                        directories: list[Path],
                        skip_hash: bool = False) -> dict:
        """
        Find duplicate files in a directory.

        Parameters:
        -----------
        directory: Path
            The path to the directory.
        skip_hash: bool
            If True, it will skip comparing the content of the files.
            Default is False.
        """
        file_sizes: dict[int, list] = {}
        duplicates: dict[int, list] = {}
        with Parallel(n_jobs=-1, return_as="generator") as parallel:
            # Find files with the same size
            results = parallel(delayed(self._get_file_size)(file_path)
                               for directory in directories
                               for file_path in directory.rglob("*")
                               if file_path.is_file()
            )
            for file_size, file_path in results:
                if file_size in file_sizes:
                    file_sizes[file_size].append(file_path)
                    # Check if first find of duplicates with this size
                    if len(file_sizes[file_size]) == 2:
                        duplicates[file_size] = file_sizes[file_size]
                else:
                    file_sizes[file_size] = [file_path]

            # Stop here if skip_hash is False
            if skip_hash:
                return duplicates

            hash_duplicates: dict[str, list] = {}
            # compare the content of the files using hashing algorithm
            results = parallel(delayed(self.hash_funct)(file_path)
                               for size, files in duplicates.items()
                               for file_path in files
            )
            
            for hash_value, file_path in results:
                if hash_value in hash_duplicates:
                    hash_duplicates[hash_value].append(file_path)
                else:
                    hash_duplicates[hash_value] = [file_path]
        # Remove entries with only one file
        hash_duplicates = {hash_str: files for hash_str, files in hash_duplicates.items()  # noqa
                           if len(files) > 1}
        return hash_duplicates
