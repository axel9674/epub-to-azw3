# epub-to-azw3

This fork expands the work done by [@iaseth](https://github.com/iaseth) by adding some QOL features like the ability to specify the output folder for the converted ebooks and parallel processing capabilities.

The original code can be found [here](https://github.com/iaseth/epub-to-azw3).

---
A simple Python script to convert all `.epub` files in a directory to `.azw3` format using Calibre's `ebook-convert` command.

## Features

- Converts `.epub` files to `.azw3` using Calibre.
- Skips conversion if the `.azw3` file already exists and is newer than the `.epub`.
- Takes the input directory path as a command-line argument.
- Takes the output directory path as an optional command-line argument (`--output_directory` / `-o`).
- Supports **parallel execution** (via flag or interactive prompt) to speed up large batch conversions with muted external tool logs.

## Requirements

- **Calibre** must be installed and `ebook-convert` should be accessible from the command line.
- Python 3.x

## Installation

Clone the repository:

```shell
git clone https://github.com/axel9674/epub-to-azw3.git
cd epub-to-azw3
```

## Usage

Run the script with:

```shell
python epub-to-azw3.py DIR [-o, --output_directory ] [[-p, --parallel] | [-s, --skip_parallel]]

positional arguments:
  DIR                           The path from which to read the input `.epub` files.
                                If the optional arg --output_directory is not specified, then
                                it is also used as the output directory path.
  
options:
  -h, --help                    show this help message and exit
  -o, --output_directory DIR    Path to the output directory
  -p, --parallel                Run conversion in parallel.
  -s, --skip_parallel           Skip the parallel execution prompt (forces sequential conversion)
```
  
### Examples:
#### Same input and output directories
The optional argument --output_directory is not specified:

```shell
python epub-to-azw3.py ~/ebooks
```
As a result, the converted books will be put in the ~/ebooks directory.

#### Specific output directory
The argument --output_directory is specified:

```shell
python epub-to-azw3.py ~/ebooks/input --output_directory ~/ebooks/output
```
As a result, the original files are read from the ~/ebooks/input directory, while the converted .azw3 files will be placed in the ~/ebooks/output directory.

Sample output:

```
[1 / 8] /mnt/mydrive/ebooks/input/Dan Simmons/Dan Simmons - The Fifth Heart.epub (1.16 MB)
    [1] Skipping /mnt/mydrive/ebooks/output/Dan Simmons/Dan Simmons - The Fifth Heart.azw3 (1.48 MB), AZW3 is up-to-date.
[2 / 8] /mnt/mydrive/ebooks/input/Dan Simmons/Dan Simmons - Drood.epub (1.03 MB)
    [2] Skipping /mnt/mydrive/ebooks/output/Dan Simmons/Dan Simmons - Drood.azw3 (1.17 MB), AZW3 is up-to-date.
[3 / 8] /mnt/mydrive/ebooks/input/Stephen King/Stephen King - IT.epub (1.78 MB)
    [3] Skipping /mnt/mydrive/ebooks/output/Stephen King/Stephen King - IT.azw3 (2.33 MB), AZW3 is up-to-date.
[4 / 8] /mnt/mydrive/ebooks/input/Stephen King/Stephen King - Pet Sematary.epub (949.53 KB)
    [4] Skipping /mnt/mydrive/ebooks/output/Stephen King/Stephen King - Pet Sematary.azw3 (1.12 MB), AZW3 is up-to-date.
[5 / 8] /mnt/mydrive/ebooks/input/Stephen King/Stephen King - Desperation.epub (1013.19 KB)
    [5] Skipping /mnt/mydrive/ebooks/output/Stephen King/Stephen King - Desperation.azw3 (1.27 MB), AZW3 is up-to-date.
[6 / 8] /mnt/mydrive/ebooks/input/Greg Egan/The Book of All Skies.epub (316.49 KB)
    [6] Skipping /mnt/mydrive/ebooks/output/Greg Egan/The Book of All Skies.azw3 (423.36 KB), AZW3 is up-to-date.
[7 / 8] /mnt/mydrive/ebooks/input/Greg Egan/Dichronauts.epub (309.50 KB)
    [7] Skipping /mnt/mydrive/ebooks/output/Greg Egan/Dichronauts.azw3 (473.31 KB), AZW3 is up-to-date.
[8 / 8] /mnt/mydrive/ebooks/input/Greg Egan/Perihelion Summer.epub (920.55 KB)
    [8] Skipping /mnt/mydrive/ebooks/output/Greg Egan/Perihelion Summer.azw3 (975.16 KB), AZW3 is up-to-date.
```

## Parallel Execution
Parallel execution can be triggered in two ways:

1. Explicitly using the -p or --parallel flag. 
2. Automatically: if the script detects more than 10 files and the flag wasn't passed, it will prompt you in the terminal asking if you want to enable parallel conversion ([y/N]).

On Unix-based systems, you can make the script executable:

```shell
chmod +x epub-to-azw3.py
./epub-to-azw3.py /path/to/directory
```

## Author

**Alessio Bollo** ([GitHub: @axel9674](https://github.com/axel9674))

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
License - see the LICENSE file for details.
