# Detailed Documentation of Features: MD2tree Decompiler and Tree2MD Recompiler

## **1. MD2tree Decompiler**
The MD2tree Decompiler converts a Markdown file into a hierarchical folder structure, with headers as folder names and content under those headers saved as `.txt` files. 

### **Key Features**
1. **Markdown Parsing**:
   - Reads a Markdown file and parses headers (`#` to `######`) to determine hierarchy levels.
   - Supports skipped heading levels by adding placeholder folders (e.g., "Placeholder Level 2").

2. **Tree Representation**:
   - Builds a hierarchical tree structure using a `Node` class.
   - Each node can represent a folder or a `.txt` file with associated content.

3. **Folder and File Creation**:
   - Creates folders and files based on the parsed Markdown structure.
   - Ensures unique folder names by appending `_N` to duplicates.

4. **Whitespace Handling**:
   - Retains original newlines and whitespace in content.
   - Deletes `.txt` files that contain only whitespace after creation.

5. **Duplicate Folder Renaming**:
   - Identifies duplicate folder names and appends `.combX` to their names.

6. **Interactive GUI**:
   - Prompts the user to select the Markdown file and output directory using Tkinter dialogs.
   - Allows the user to decide whether to add a delay between folder/file creation and handle duplicate folder renaming.

7. **Estimated Time Display**:
   - Calculates and displays the estimated time for structure creation based on the number of folders and files.

### **Workflow**
1. **Select a Markdown File**:
   - User selects a `.md` file for conversion.
2. **Parse Markdown**:
   - Headers become folder names, and content becomes `.txt` files.
3. **Choose Output Directory**:
   - User selects the root folder for saving the generated structure.
4. **Create Structure**:
   - Folders and files are created based on the parsed Markdown.
5. **Rename Duplicates**:
   - Optionally renames duplicate folders with a `.combX` suffix.

---

## **2. Tree2MD Recompiler**
The Tree2MD Recompiler reverses the process of the MD2tree Decompiler. It converts a hierarchical folder structure back into a Markdown document.

### **Key Features**
1. **Folder Traversal**:
   - Recursively traverses a folder structure to reconstruct Markdown headers and content.
   - Includes `.combX` folders as combined headers with corresponding content.

2. **Markdown Conversion**:
   - Folder names are treated as headers, with their level determined by the folder depth.
   - Content from `.txt` files is added under the corresponding headers.

3. **Combining `.combX` Folders**:
   - Handles `.combX` folders by grouping them under a single base header (e.g., `FolderName.comb0` and `FolderName.comb1` become `FolderName`).

4. **Output Customization**:
   - Allows the user to specify the root folder header level (e.g., `#`, `##`).
   - Orders entries by creation time for consistent results.

5. **Interactive GUI**:
   - Uses Tkinter dialogs to let the user:
     - Select the root folder to convert.
     - Set the root folder's header level.
     - Choose the output Markdown file's save location.

6. **Error Handling**:
   - Gracefully handles invalid selections (e.g., canceling folder selection or save dialogs).
   - Avoids processing files that are not `.txt`.

### **Workflow**
1. **Select Root Folder**:
   - User selects a folder structure for reconstruction.
2. **Choose Header Level**:
   - User specifies the Markdown header level for the root folder.
3. **Traverse Folder Structure**:
   - Processes subfolders as headers and `.txt` files as content.
4. **Save Markdown File**:
   - Prompts the user to choose a save location for the reconstructed Markdown.

---

## **Comparison of Features**

| Feature                              | MD2tree Decompiler                         | Tree2MD Recompiler                         |
|--------------------------------------|--------------------------------------------|--------------------------------------------|
| **Primary Function**                 | Converts Markdown to folder structure.     | Converts folder structure to Markdown.     |
| **Input**                            | Markdown file (`.md`).                     | Root folder containing hierarchical data.  |
| **Output**                           | Folder structure with `.txt` files.        | Markdown file (`.md`).                     |
| **Header Parsing**                   | Handles `#` to `######` headers.           | Converts folder depth to Markdown headers. |
| **Whitespace Retention**             | Retains and handles empty lines.           | Includes content from `.txt` files.        |
| **Combining `.combX` Folders**       | Renames duplicate folders to `.combX`.     | Groups `.combX` folders under single header. |
| **Interactive GUI**                  | File and folder selection, rename options. | Folder selection, header level, save path. |
| **Error Handling**                   | Handles missing files, duplicate folders.  | Handles invalid selections, empty folders. |

---

## **Usage Scenarios**
- **MD2tree Decompiler**:
  - Preparing structured data from Markdown for use in file-based workflows.
  - Automating folder generation for hierarchical content management.

- **Tree2MD Recompiler**:
  - Rebuilding Markdown documents from file-based content.
  - Converting file system structures back into editable Markdown for documentation or publishing.
