import tkinter as tk
from tkinter import filedialog
import html2text

def select_input_file():
    file_path = filedialog.askopenfilename(
        title="Select HTML File",
        filetypes=[("HTML Files", "*.html;*.htm"), ("All Files", "*.*")]
    )
    return file_path

def select_output_file():
    file_path = filedialog.asksaveasfilename(
        title="Save Markdown File As",
        defaultextension=".md",
        filetypes=[("Markdown Files", "*.md"), ("All Files", "*.*")]
    )
    return file_path

def get_user_preferences():
    print("Do you want to ignore links in the Markdown output? (yes/no)")
    ignore_links = input().strip().lower() == "yes"

    print("Do you want to ignore images in the Markdown output? (yes/no)")
    ignore_images = input().strip().lower() == "yes"

    return ignore_links, ignore_images

def convert_html_to_markdown(input_file, output_file, ignore_links, ignore_images):
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            html_content = f.read()
        markdown_converter = html2text.HTML2Text()
        markdown_converter.ignore_links = ignore_links
        markdown_converter.ignore_images = ignore_images
        markdown_content = markdown_converter.handle(html_content)
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(markdown_content)
        print(f"Conversion successful! Markdown file saved at: {output_file}")
    except Exception as e:
        print(f"An error occurred during conversion: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  # Hide the root window

    input_file = select_input_file()
    if not input_file:
        print("No input file selected. Exiting.")
        exit()

    output_file = select_output_file()
    if not output_file:
        print("No output file selected. Exiting.")
        exit()

    # Get user preferences for ignoring links and images
    ignore_links, ignore_images = get_user_preferences()

    convert_html_to_markdown(input_file, output_file, ignore_links, ignore_images)
