import filedup
from pathlib import Path
import timeit
import time
import logging


def main():
    """
    Demo of the DuplicateFileLocator class to find duplicate files in a
    directory. Hardcoded start directory.
    """

    # Set base directory
    base_dir = Path("C:\\Temp\\")

    # Create a DuplicateFileLocator object
    dup_locator = filedup.DuplicateFileLocator()

    # Find duplicates in the base directory
    duplicates = dup_locator.find_duplicates(base_dir)

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
    logging.info("Start processing...")
    main()
    # measure time of execution
    stop = timeit.default_timer()
    # print time of execution in h:min:s
    logging.info(f"Processing done in {time.strftime('%H:%M:%S', time.gmtime(stop-start))} (h:min:s)")  # noqa
