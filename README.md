### README

# Markdown to Tree and Tree to Markdown Utilities

This repository contains two scripts for converting between Markdown (`.md`) files and folder structures. These scripts were originally developed for personal use, were created using AI assistance, and are licensed under the **GPL-3.0** license.

---

## Overview

### Script 1: `MD2tree_decompiler.py`
**Purpose**: Converts a Markdown file into a corresponding folder and file structure.

- **Headers** (`#`, `##`, etc.) are converted to folders.
- Content under headers without sub-headers is stored in `.txt` files.
- Handles duplicate `.txt` filenames by appending `.combX.txt` suffixes (where `X` is a numeric counter).
- If a skipped level is detected (e.g., # followed by ###), the script automatically creates placeholder nodes for the missing levels.

### Script 2: `tree2MD_recompiler.py`
**Purpose**: Converts a folder and file structure back into a Markdown file.

- Combines the contents of `.comb.txt` and `.combX.txt` files into their parent header.
- Allows specification of the Markdown header level (`#`, `##`, etc.) for the root folder.
- Outputs a Markdown file that faithfully represents the input structure.

---

## Features

### `MD2tree_decompiler.py`
- Converts Markdown headers into folders and `.txt` files.
- Optionally adds a 1-second delay during creation to ensure unique timestamps.
- Detects duplicate `.txt` filenames and renames them with `.combX.txt` suffixes.

### `tree2MD_recompiler.py`
- Traverses folder structures to generate a Markdown file.
- Combines content from `.comb.txt` and `.combX.txt` files under their parent headers.
- Allows sorting by file creation time.

---

## Installation

1. Clone this repository:
   ```bash
   git clone <repository_url>
   cd <repository_folder>
   ```
2. Ensure you have Python 3 installed on your system.

3. Install dependencies if needed:
   ```bash
   pip install -r requirements.txt
   ```
   *(No additional dependencies required for now, but `tkinter` is included by default in most Python installations.)*

---

## Usage

### `MD2tree_decompiler.py`
1. Run the script:
   ```bash
   python MD2tree_decompiler.py
   ```
2. Select a Markdown file via the file dialog.
3. Choose a root folder where the structure will be created.
4. Optionally add a delay to ensure unique timestamps.
5. Decide if duplicate `.txt` filenames should be renamed with `.combX.txt` suffixes.

**Example**:
- **Markdown File**:
  ```markdown
  # Root
  ## Subfolder1
  ### Subfolder1.1
  Some content here.
  ## Subfolder2
  Text for Subfolder2.
  ```
- **Output Structure**:
  ```
  Root/
  ├── Subfolder1/
  │   └── Subfolder1.1.txt
  └── Subfolder2.txt
  ```

---

### `tree2MD_recompiler.py`
1. Run the script:
   ```bash
   python tree2MD_recompiler.py
   ```
2. Select the root folder of the structure via the file dialog.
3. Specify the Markdown header level (`#`, `##`, etc.) for the root folder.
4. Choose a location to save the reconstructed Markdown file.

**Example**:
- **Folder Structure**:
  ```
  Root/
  ├── Subfolder1/
  │   ├── file1.comb0.txt (contains "Part 1.")
  │   └── file1.comb1.txt (contains "Part 2.")
  └── Subfolder2.txt (contains "Other content.")
  ```
- **Reconstructed Markdown**:
  ```markdown
  # Root
  ## Subfolder1
  Part 1.

  Part 2.

  ## Subfolder2
  Other content.
  ```

---

## License

This project is licensed under the **GNU General Public License v3.0 (GPL-3.0)**. For more information, see the [LICENSE](LICENSE) file or visit https://www.gnu.org/licenses/gpl-3.0.html.

---

## Acknowledgments

These scripts were:
- **Originally created for personal use**.
- **Developed using AI assistance** to improve functionality and usability.
- I just feel safer having this stuff in the github cloud, rather than my own messy storage.

Feel free to modify and adapt them for your own needs under the terms of the GPL-3.0 license.