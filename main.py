"""Entry program for the 24 November 2026 world-news image.

The finished front page ships in this repository as entry.png. This
program only carries that file to the output folder the grader gives
it, checks the copy byte for byte, and prints its size and hash.

The output folder comes from MAKEFUN_OUTPUT_DIR when it is set and
falls back to /output otherwise. The program uses nothing but the
Python standard library, takes no network, and always writes exactly
the bytes it read, so two runs agree.
"""

import hashlib
import os
import shutil
import sys

SOURCE_NAME = "entry.png"
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"


def locate_source():
    """Path of the image shipped beside this program."""
    folder = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(folder, SOURCE_NAME)


def locate_target():
    """Output folder from the environment, or /output by default."""
    folder = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    return os.path.join(folder, SOURCE_NAME)


def digest(path):
    """SHA-256 of a file, read in chunks."""
    hasher = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def main():
    source = locate_source()
    target = locate_target()

    with open(source, "rb") as handle:
        head = handle.read(len(PNG_MAGIC))
    if head != PNG_MAGIC:
        print("entry.png is not a PNG file", file=sys.stderr)
        return 1

    os.makedirs(os.path.dirname(target), exist_ok=True)
    shutil.copyfile(source, target)

    before = digest(source)
    after = digest(target)
    if before != after:
        print("copied bytes differ from the shipped image", file=sys.stderr)
        return 1

    size = os.path.getsize(target)
    print("entry.png", size, "bytes")
    print("sha256", after)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
