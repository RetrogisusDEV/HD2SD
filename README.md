# HD2SD

Skin Converter For OSU!
 
- Original C# version (c) [Jose134](https://github.com/Jose134/HDtoSD)  
- Python adaptation developed by [Me](https://github/RetrogisusDEV)

This program automatically converts all `@2x` files in your osu! skin folder to SD resolution by resizing them to half their original dimensions.

## Features

- Batch conversion of all `@2x` images to SD resolution
- Option to replace existing SD files or skip them
- Support for JPG and PNG formats
- Recursive subdirectory search
- Rainbow color mode for fun console output

## Usage

Place the executable in your osu! skin folder and run it with optional parameters:

| Parameter          | Short Form | Values       | Description |
|--------------------|------------|--------------|-------------|
| `--replace`        | `-r`       | -            | Replace existing SD files instead of skipping them |
| `--copy`           | `-cp`      | -            | Copy empty images (1x1px) instead of renaming |
| `--color`          | `-c`       | -            | Enable rainbow color mode in console |
| `--subdirs`        | `-s`       | `true/false` | Enable/disable subdirectory search |
| `--help`           | `-h`       | -            | Show help information |

## Basic Examples

```bash
# Basic conversion (skips existing SD files)
HD2SD.exe

# Replace all existing SD files
HD2SD.exe --replace

# Search in subdirectories and enable rainbow mode
HD2SD.exe --subdirs true --color
```

## Important Notes
### Location Requirement:
- The program must be placed directly in your osu! skin folder as it searches for images in the same directory where the executable is located.

- Supported Formats:
Currently supports `.jpg` and `.png` files with `@2x` suffix (e.g., `hitcircle@2x.png` → `hitcircle.png`)

- Empty Images:
By default, 1x1px images will be renamed (not copied) to their SD version unless `--copy` is specified.

## Troubleshooting
- If files aren't being converted, ensure:

- - The program is in your skin folder

- - Your files use the correct @2x naming convention

- - You have proper file permissions

- - The images aren't already converted and you're not using `--replace`

- For color issues in console, try running in a different terminal or without `--color`
