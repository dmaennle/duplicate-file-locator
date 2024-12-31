import filedup
from pathlib import Path
import timeit
import time
import logging
import argparse
import sys


def main():
    """
    Demo of the DuplicateFileLocator class to find duplicate files in a
    directory. Hardcoded start directory.
    """

    parser = argparse.ArgumentParser(add_help=True)
    parser.add_argument(
        "paths",
        nargs="*",
        help="List of folders to scan for duplicates."
    )
    args = parser.parse_args()

    # Check for help arguments
    if (not args.paths or
        args.paths[0].lower() in ["help","-h","--h","-help","--help","/?","/h","/help"]):
        parser.print_help()
        sys.exit(0)

    # Validate directories
    directories = []
    for p in args.paths:
        path = Path(p)
        if not path.is_dir():
            print(f"Error: The path '{p}' does not exist or is not a directory.")
            sys.exit(1)
        directories.append(path)

    # Create a DuplicateFileLocator object
    dup_locator = filedup.DuplicateFileLocator()

    # Find duplicates in the directories
    duplicates = dup_locator.find_duplicates(directories)

    # Print the duplicates using logging
    for hash, files in duplicates.items():
        logging.info(f"Duplicate files with hash {hash}:")
        for file in files:
            logging.info(f"  {file}")


if __name__ == "__main__":
    # config basic logging
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")

    # measure time of execution
    start = timeit.default_timer()
    logging.debug("Start processing...")
    main()
    # measure time of execution
    stop = timeit.default_timer()
    # print time of execution in h:min:s
    logging.info(f"Processing done in {time.strftime('%H:%M:%S', time.gmtime(stop-start))} (h:min:s)")  # noqa
