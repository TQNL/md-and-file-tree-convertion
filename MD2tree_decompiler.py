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
        """Display the tree structure including folders and .txt files."""
        connector = "└── " if is_last else "├── "
        print(prefix + connector + self.name)

        # Print the .txt file if there is content
        if self.content.strip():
            txt_connector = "    " if is_last else "│   "
            print(prefix + txt_connector + f"└── {self.name}.txt")

        prefix += "    " if is_last else "│   "
        for i, child in enumerate(self.children):
            child.display(prefix, is_last=(i == len(self.children) - 1))

    def count_elements(self):
        """Count the total number of folders and files in the tree."""
        count = 0  # Initialize the count

        def counter(node):
            nonlocal count  # Use 'count' from the enclosing scope
            count += 1  # Count the current node
            if node.content.strip():  # If there is content, count the corresponding .txt file
                count += 1
            for child in node.children:  # Recursively count children
                counter(child)

        counter(self)
        return count

    def create_structure(self, base_path, add_delay=False):
        """Recursively create folders or files based on the structure."""
        folder_name = self.name
        folder_path = os.path.join(base_path, folder_name)

        # Track used names in the current directory to handle duplicates
        used_names = set(os.listdir(base_path))

        # Ensure unique folder name by appending `_N` if needed
        counter = 1
        while folder_name in used_names:
            folder_name = f"{self.name}_{counter}"
            folder_path = os.path.join(base_path, folder_name)
            counter += 1

        # Create the folder
        os.makedirs(folder_path, exist_ok=True)
        if add_delay:
            time.sleep(1)  # Add 1-second delay

        # Save content as a .txt file if it exists
        if self.content.strip():
            txt_file_path = os.path.join(folder_path, f"{self.name}.txt")
            with open(txt_file_path, "w", encoding="utf-8") as file:
                file.write(self.content.strip())
            if add_delay:
                time.sleep(1)  # Add 1-second delay

        # Create subfolders or files for children
        for child in self.children:
            child.create_structure(folder_path, add_delay)


def rename_duplicate_folders(root_folder):
    """Rename duplicate folder names by appending `.combX` to each instance."""
    folder_names = {}  # Dictionary to track folder names and their occurrences

    # First pass: Traverse the structure and collect folder names
    for dirpath, dirnames, _ in os.walk(root_folder, topdown=False):
        for foldername in dirnames:
            if foldername not in folder_names:
                folder_names[foldername] = []
            folder_names[foldername].append(os.path.join(dirpath, foldername))

    # Second pass: Rename duplicates
    for foldername, paths in folder_names.items():
        if len(paths) > 1:  # Only process duplicates
            for i, path in enumerate(paths):
                new_name = f"{foldername}.comb{i}"
                new_path = os.path.join(os.path.dirname(path), new_name)
                os.rename(path, new_path)


def parse_markdown(markdown_text):
    """Parse a Markdown file into a hierarchical structure with placeholders for skipped levels."""
    lines = markdown_text.splitlines()
    header_pattern = re.compile(r"^(#{1,6})\s+(.*)$")

    root_node = Node("Selected Root")
    current_nodes = {0: root_node}  # Tracks the current node at each level

    for line in lines:
        match = header_pattern.match(line)
        if match:
            level = len(match.group(1))  # Number of '#' determines the level
            header_text = match.group(2).strip()

            # Dynamically add placeholder nodes for skipped levels
            if level - 1 not in current_nodes:
                for missing_level in range(1, level):
                    if missing_level not in current_nodes:
                        placeholder_node = Node(f"Placeholder Level {missing_level}")
                        parent_node = current_nodes[missing_level - 1]
                        parent_node.add_child(placeholder_node)
                        current_nodes[missing_level] = placeholder_node

            # Create the current node
            new_node = Node(header_text)
            parent_node = current_nodes[level - 1]
            parent_node.add_child(new_node)
            current_nodes[level] = new_node

            # Remove nodes deeper than the current level
            for deeper_level in range(level + 1, 7):
                current_nodes.pop(deeper_level, None)
        else:
            # Add content to the last valid header
            if current_nodes:
                current_nodes[max(current_nodes.keys())].content += line.strip() + "\n"

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
    estimated_time = int(total_elements)

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

    # Step 8: Ask user if they want to rename duplicate folders
    rename_folders = askyesno(
        "Rename Duplicate Folders",
        (
            "WARNING: Ensure that the root folder does not contain unrelated folders.\n"
            "Unrelated folders with duplicate names may also be renamed with a `.combX` suffix.\n\n"
            "Do you want to identify and rename duplicate folders?"
        )
    )
    if rename_folders:
        rename_duplicate_folders(root_folder)
        print("Duplicate folders have been renamed with `.combX` suffixes.")


if __name__ == "__main__":
    main()
