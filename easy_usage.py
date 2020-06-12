#!/usr/bin/env python3
"""Easy usage example for ffms2."""

import os
import sys
import time
import ffms2.console_mode

ROOT_DIR = os.path.dirname(sys.argv[0])
ACCEPTABLE_DELAY = 0.03


def main():
    source_path = os.path.join(ROOT_DIR, "ffms2", "data", "morning rescue.mkv")
    now = time.time()
    vs = ffms2.VideoSource(source_path)
    if vs.index.index_file:
        if (
            delay > ACCEPTABLE_DELAY
        ):  # If opening a file has a delay greater than ACCEPTABLE_DELAY, create an index file
            vs.index.write()
            print(
                f"The next time you open `{source_path}` the ffms2 will use the index file `{vs.index.index_file}`"
            )
            print(
                f"since without it the opening delay `{delay}` is greater then `{ACCEPTABLE_DELAY}`"
            )
        else:
            print(
                f"The next time you open `{source_path}` the ffms2 will not use the index file"
            )
            print(
                f"since even without it the opening delay `{delay}` is less then `{ACCEPTABLE_DELAY}`"
            )


if __name__ == "__main__":
    sys.exit(main())
