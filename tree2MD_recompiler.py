# tree2MD_recompiler
# Copyright (C) 2024 TQNL
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.

## `*.comb` folder are the same as direct txt-files, remove
## those folders should give their combined name as a new header

import os
import re
from tkinter import Tk
from tkinter.filedialog import askdirectory, asksaveasfilename
from tkinter.simpledialog import askinteger


def folder_to_markdown(folder_path, level=1):
    """Recursively traverse the folder structure and reconstruct Markdown."""
    markdown_lines = []

    # Regex to match `.combX` folder names
    comb_pattern = re.compile(r"^(.*)\.comb(\d+)$")  # Captures base name and numeric suffix

    # Get entries sorted by creation time
    entries = sorted(
        os.listdir(folder_path),
        key=lambda e: os.path.getctime(os.path.join(folder_path, e))
    )

    combined_folders = {}  # Dictionary to group `.combX` folders by base name

    for entry in entries:
        entry_path = os.path.join(folder_path, entry)

        if os.path.isdir(entry_path):
            match = comb_pattern.match(entry)
            if match:
                # Group `.combX` folders by their base name
                base_name = match.group(1)
                if base_name not in combined_folders:
                    combined_folders[base_name] = []
                combined_folders[base_name].append(entry_path)
            else:
                # Regular folder names become headers
                markdown_lines.append(f"{'#' * level} {entry}")
                markdown_lines.extend(folder_to_markdown(entry_path, level + 1))
        elif entry.endswith(".txt"):
            # Regular .txt files represent content for the folder header
            with open(entry_path, "r", encoding="utf-8") as file:
                content = file.read().strip()
            if content:
                if markdown_lines and not markdown_lines[-1].endswith("<br>"):
                    # Append a blank line with <br> before new content, if not already present
                    markdown_lines.append("<br>")
                markdown_lines.append(content)

    # Process grouped `.combX` folders
    for base_name, paths in combined_folders.items():
        markdown_lines.append(f"{'#' * level} {base_name}")  # Combined header
        for path in paths:
            markdown_lines.extend(folder_to_markdown(path, level + 1))

    return markdown_lines


def main():
    Tk().withdraw()  # Hide the root Tkinter window

    # Step 1: Select the root folder of the structure
    folder_path = askdirectory(title="Select the Folder Structure to Reconstruct")
    if not folder_path:
        print("No folder selected. Exiting.")
        return

    # Step 2: Choose the header level for the root folder
    header_level = askinteger(
        "Header Level",
        "Enter the header level for the root folder (e.g., 1 for '#'):",
        minvalue=1,
        maxvalue=6
    )
    if header_level is None:
        print("No header level specified. Exiting.")
        return

    # Step 3: Choose the output file location
    save_path = asksaveasfilename(
        title="Save Reconstructed Markdown File",
        defaultextension=".md",
        filetypes=[("Markdown files", "*.md"), ("All files", "*.*")]
    )
    if not save_path:
        print("No save location selected. Exiting.")
        return

    # Extract the root folder name
    root_folder_name = os.path.basename(folder_path.rstrip(os.sep))

    # Convert the folder structure to Markdown
    markdown_lines = [f"{'#' * header_level} {root_folder_name}"]  # Root folder header
    markdown_lines.extend(folder_to_markdown(folder_path, level=header_level + 1))

    # Step 4: Save the Markdown file
    try:
        with open(save_path, "w", encoding="utf-8") as file:
            file.write("\n".join(markdown_lines).strip())
        print(f"Markdown file successfully reconstructed and saved to: {save_path}")
    except Exception as e:
        print(f"Error saving the Markdown file: {e}")


if __name__ == "__main__":
    main()
