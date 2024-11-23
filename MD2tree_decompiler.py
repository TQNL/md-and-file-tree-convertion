# MD2tree_decompiler
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

import re
import os
import time
from tkinter import Tk
from tkinter.filedialog import askopenfilename, askdirectory
from tkinter.messagebox import askyesno


class Node:
    def __init__(self, name, content=""):
        self.name = name
        self.children = []
        self.content = content  # Stores the text under the header

    def add_child(self, child):
        self.children.append(child)

    def display(self, prefix="", is_last=True):
        """Display the tree structure using branching characters."""
        connector = "└── " if is_last else "├── "
        print(prefix + connector + self.name)
        prefix += "    " if is_last else "│   "
        for i, child in enumerate(self.children):
            child.display(prefix, is_last=(i == len(self.children) - 1))

    def count_elements(self):
        """Count the total number of folders and files in the tree."""
        count = 1 if not self.children else 0  # Count as a file if it's a leaf
        for child in self.children:
            count += child.count_elements()
        return count

    def create_structure(self, base_path, add_delay=False):
        """Recursively create folders or files based on the structure."""
        if self.children:
            # Create a folder for this node if it has children
            current_path = os.path.join(base_path, self.name)
            os.makedirs(current_path, exist_ok=True)
            if add_delay:
                time.sleep(1)  # Add 1-second delay
            for child in self.children:
                child.create_structure(current_path, add_delay)
        else:
            # Create a .txt file for this leaf node in the parent folder
            txt_file_path = os.path.join(base_path, f"{self.name}.txt")
            with open(txt_file_path, "w", encoding="utf-8") as file:
                file.write(self.content.strip())
            if add_delay:
                time.sleep(1)  # Add 1-second delay


def identify_duplicate_files(root_folder):
    """Identify all duplicate file names across the folder structure."""
    file_counts = {}

    # First pass: Count occurrences of each file name (without extension)
    for dirpath, _, filenames in os.walk(root_folder):
        for filename in filenames:
            if filename.endswith(".txt") and not filename.endswith(".comb.txt"):
                name_without_extension = os.path.splitext(filename)[0]
                file_counts[name_without_extension] = file_counts.get(name_without_extension, 0) + 1

    # Find names with more than one occurrence
    duplicates = {name for name, count in file_counts.items() if count > 1}
    return duplicates


def rename_duplicate_txt_files(root_folder, duplicates):
    """Rename all duplicate .txt files to .comb.txt with numeric suffix."""
    suffix_counts = {}  # Track the numeric suffix for each duplicate name

    # Second pass: Rename duplicate files
    for dirpath, _, filenames in os.walk(root_folder):
        for filename in filenames:
            if filename.endswith(".txt") and not filename.endswith(".comb.txt"):
                name_without_extension = os.path.splitext(filename)[0]

                if name_without_extension in duplicates:
                    # Increment the suffix count
                    suffix = suffix_counts.get(name_without_extension, 0)
                    suffix_counts[name_without_extension] = suffix + 1

                    # Rename the file with a numeric suffix
                    old_path = os.path.join(dirpath, filename)
                    new_name = f"{name_without_extension}.comb{suffix}.txt"
                    new_path = os.path.join(dirpath, new_name)
                    os.rename(old_path, new_path)


def parse_markdown(markdown_text):
    """Parse a Markdown file into a hierarchical structure."""
    lines = markdown_text.splitlines()
    header_pattern = re.compile(r"^(#{1,6})\s+(.*)$")

    root_node = Node("Selected Root")
    current_nodes = {0: root_node}

    current_content = []  # To accumulate text under a header

    for line in lines:
        match = header_pattern.match(line)
        if match:
            # Save accumulated content for the previous header
            if current_content and level in current_nodes:
                current_nodes[level].content = "\n".join(current_content).strip()
                current_content = []

            # Process the new header
            level = len(match.group(1))  # Number of '#' determines the level
            header_text = match.group(2).strip()

            new_node = Node(header_text)
            parent_node = current_nodes.get(level - 1, root_node)
            parent_node.add_child(new_node)
            current_nodes[level] = new_node

            # Remove any deeper nodes that are no longer relevant
            for deeper_level in range(level + 1, 7):
                current_nodes.pop(deeper_level, None)
        else:
            # Accumulate content for the current header
            current_content.append(line)

    # Handle the last accumulated content
    if current_content and level in current_nodes:
        current_nodes[level].content = "\n".join(current_content).strip()

    return root_node


def main():
    Tk().withdraw()  # Hide the root Tkinter window

    # Step 1: Select a Markdown file
    markdown_file = askopenfilename(
        title="Select a Markdown File",
        filetypes=[("Markdown files", "*.md"), ("All files", "*.*")]
    )
    if not markdown_file:
        print("No Markdown file selected. Exiting.")
        return

    # Step 2: Read the Markdown file
    try:
        with open(markdown_file, "r", encoding="utf-8") as f:
            markdown_content = f.read()
    except Exception as e:
        print(f"Error reading the Markdown file: {e}")
        return

    # Step 3: Parse the Markdown file
    tree = parse_markdown(markdown_content)
    print("\nMarkdown Structure Tree:")
    tree.display()

    # Step 4: Count the total elements (folders and files) to estimate time
    total_elements = tree.count_elements()
    estimated_time = int(total_elements * 1.3)  # Multiply by 1.3 for accuracy

    # Step 5: Select the root folder for creating the structure
    root_folder = askdirectory(title="Select a Root Folder for Folder Structure")
    if not root_folder:
        print("No root folder selected. Exiting.")
        return

    # Step 6: Prompt the user with the time estimate
    add_delay = askyesno(
        "Add Delay",
        f"Estimated time with delay: {estimated_time} seconds.\nAdd delay?"
    )

    # Step 7: Create the folder and file structure
    try:
        print("\nCreating folder structure...")
        for child in tree.children:  # Start creating folders from top-level nodes
            child.create_structure(root_folder, add_delay=add_delay)
        print(f"Folder structure created successfully in: {root_folder}")
    except Exception as e:
        print(f"Error creating folder structure: {e}")
        return

    # Step 8: Identify and rename duplicate .txt files
    rename_files = askyesno(
        "Rename Files",
        "Do you want to rename all duplicate .txt files to .comb.txt with numeric suffix?"
    )
    if rename_files:
        duplicates = identify_duplicate_files(root_folder)
        rename_duplicate_txt_files(root_folder, duplicates)
        print("Renaming of duplicate .txt files completed.")


if __name__ == "__main__":
    main()
