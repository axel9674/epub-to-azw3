#!/usr/bin/env python3

import argparse
import os
import subprocess
from concurrent.futures import ThreadPoolExecutor


def get_size(path):
    if not os.path.isfile(path):
        return "NULL"

    size = os.path.getsize(path)  # Get file size in bytes

    for unit in ['bytes', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024:
            return f"{size:.2f} {unit}"
        size /= 1024

    return f"{size:.2f} PB"  # Handle extremely large files


def _colorize(color_code, *args, sep=' '):
    text = sep.join(map(str, args))
    return f"\033[{color_code}m{text}\033[0m"


def red(*args, sep=' '):
    return _colorize(31, *args, sep=sep)


def green(*args, sep=' '):
    return _colorize(32, *args, sep=sep)


def yellow(*args, sep=' '):
    return _colorize(33, *args, sep=sep)


def blue(*args, sep=' '):
    return _colorize(34, *args, sep=sep)


class EpubEbook:
    def __init__(self, root, output_directory, filename, app):
        self.root = root
        self.output_directory = output_directory
        self.filename = filename
        self.idx = app.count
        self.app = app
        self.epub_path = os.path.join(root, filename)
        self.azw3_path = os.path.join(output_directory, os.path.splitext(filename)[0] + ".azw3")

    def azw3_exists(self):
        if os.path.exists(self.azw3_path) and os.path.getmtime(self.azw3_path) > os.path.getmtime(self.epub_path):
            return True
        return False

    def convert_epub_to_azw3(self, force=False):
        print(f"[{self.idx + 1} / {self.app.count}] {blue(self.epub_path)} ({yellow(get_size(self.epub_path))})")
        if not force and self.azw3_exists():
            # Skip conversion if AZW3 exists and is newer than EPUB
            print(f"\t[{self.idx + 1}] Skipping {green(self.azw3_path)} ({yellow(get_size(self.azw3_path))}), AZW3 is up-to-date.")
            return

        print(f"\t[{self.idx + 1}] Converting {yellow(self.filename)} to AZW3...")
        subprocess.run(["ebook-convert", self.epub_path, self.azw3_path], check=True, stdout=subprocess.DEVNULL)
        print(f"\t[{self.idx + 1}] Conversion completed: {green(self.azw3_path)} ({yellow(get_size(self.azw3_path))})")


class ConvertApp:
    def __init__(self, directory, output_directory=None, parallel=False, skip_parallel=False):
        self.directory = directory
        self.output_directory = output_directory or directory
        self.parallel = parallel
        self.skip_parallel = skip_parallel
        self.setup_epubs()

    @property
    def count(self):
        return len(self.epubs)

    def setup_epubs(self):
        self.epubs = []
        for root, _, files in os.walk(self.directory):
            for filename in files:
                if filename.lower().endswith(".epub"):
                    epub = EpubEbook(root, self.output_directory, filename, self)
                    self.epubs.append(epub)

    def create_output_directory(self):
        if not os.path.exists(self.output_directory) and self.output_directory is not None:
            os.mkdir(self.output_directory)

    def convert_epub_to_azw3(self):
        self.create_output_directory()

        if self.count == 0:
            print(yellow(f"No EPUB files to convert in the {self.directory} directory."))
            return

        THRESHOLD = 1
        if not self.parallel and self.count > THRESHOLD and not self.skip_parallel:
            print(yellow(f"Found {self.count} EPUB files."))
            choice = input(blue("Do you want to use parallel convertion to speed up the process? [y/N]")).strip().lower()
            if choice in ['s', 'si', 'sì', 'y', 'yes']:
                self.parallel = True

        if self.parallel and self.count > 0:
            max_workers = os.cpu_count() or 4
            print(blue(f"Starting the parallel conversion using {max_workers} workers..."))

            with ThreadPoolExecutor(max_workers=max_workers) as executor:
                executor.map(lambda epub: epub.convert_epub_to_azw3(), self.epubs)
        else:
            for epub in self.epubs:
                epub.convert_epub_to_azw3()


def main():
    parser = argparse.ArgumentParser(description="Convert all EPUB files in a directory to AZW3 using Calibre's ebook-convert.")
    parser.add_argument("directory", metavar="DIR", type=str, help="Path to the directory containing EPUB files")
    parser.add_argument("-o", "--output_directory", metavar="DIR", type=str, help="Path to the output directory")

    parallel_group = parser.add_mutually_exclusive_group()
    parallel_group.add_argument("-p", "--parallel", action="store_true", help="Run conversion in parallel.")
    parallel_group.add_argument("-s", "--skip_parallel", action="store_true", help="Skip the parallel execution prompt (force sequential)")
    args = parser.parse_args()

    app = ConvertApp(directory=args.directory, output_directory=args.output_directory, parallel=args.parallel, skip_parallel=args.skip_parallel)
    app.convert_epub_to_azw3()


if __name__ == "__main__":
    main()
