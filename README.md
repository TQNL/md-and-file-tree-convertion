### README

# Markdown to Tree and Tree to Markdown Utilities

This repository contains two scripts for converting between Markdown (`.md`) files and folder structures. These scripts were originally developed for personal use, were created using AI assistance, and are licensed under the **GPL-3.0** license.

---

## Overview
This repository contains two complementary tools:
1. **MD2tree Decompiler**: Converts a Markdown file into a hierarchical folder structure.
2. **Tree2MD Recompiler**: Reconstructs a Markdown file from a folder structure.

---

## MD2tree Decompiler
### Features
- **Markdown Parsing**:
  - Converts headers (`#` to `######`) into folders.
  - Saves content under headers as `.txt` files.
- **Folder and File Handling**:
  - Ensures unique folder names by appending `_N` to duplicates.
  - Deletes `.txt` files that only contain whitespace.
- **Interactive Workflow**:
  - Select input Markdown file and output directory.
  - Optionally rename duplicate folders with `.combX`.
- **Tree Representation**:
  - Displays the structure in a tree-like format.

### Workflow
1. Select a Markdown file.
2. Parse the file into folders and `.txt` files.
3. Choose an output directory.
4. Create the folder structure with optional delays and duplicate handling.

---

## Tree2MD Recompiler
### Features
- **Folder Traversal**:
  - Converts folder names to headers based on folder depth.
  - Groups `.combX` folders under a single header.
- **Content Handling**:
  - Includes `.txt` file content as Markdown under corresponding headers.
- **Interactive Workflow**:
  - Select root folder and output Markdown file.
  - Specify the header level for the root folder.

### Workflow
1. Select a folder structure.
2. Specify the root folder’s header level.
3. Save the reconstructed Markdown file.

---

## Use Cases
- **MD2tree Decompiler**:
  - Convert Markdown to a folder structure for project organization or content management.
- **Tree2MD Recompiler**:
  - Recreate Markdown documents from hierarchical folder structures for documentation or publishing.

---

## Getting Started
1. Run the desired script (`MD2tree_decompiler.py` or `tree2MD_recompiler.py`).
2. Follow the interactive prompts.
3. Review and use the output (folder structure or Markdown file).

---

## License
Both tools are licensed under the GNU General Public License v3.0. See [GNU License](https://www.gnu.org/licenses/) for details.