import os


def replace_all(old, new, source_path, dest_path):
    """
    Reads the contents of the source file, replaces all occurrences of
    'old' with 'new', and writes the result to the destination file.
    """
    # Read the contents of the source file
    try:
        with open(source_path, 'r') as reader:
            content = reader.read()
    except FileNotFoundError:
        print(f"Error: Source file '{source_path}' not found.")
        return
    except IOError as e:
        print(f"Error reading file '{source_path}': {e}")
        return

    # Replace the old string with the new
    modified_content = content.replace(old, new)

    # Ensure the destination directory exists
    dest_dir = os.path.dirname(dest_path)
    if dest_dir and not os.path.exists(dest_dir):
        os.makedirs(dest_dir, exist_ok=True)
        print(f"Created directory: {dest_dir}")

    # Write the result into the destination file
    try:
        with open(dest_path, 'w') as writer:
            writer.write(modified_content)
        print(f"Successfully replaced all occurrences of '{old}' in '{source_path}' and wrote to '{dest_path}'.")
    except IOError as e:
        print(f"Error writing to file '{dest_path}': {e}")


# --- Test Case ---

# 1. Ensure the 'photos' directory exists
os.makedirs("photos", exist_ok=True)

# 2. Create the source file for testing
with open("photos/notes.txt", "w") as f:
    f.write("View the photos in the photos directory. Some photos are missing.")

# 3. Call the function with the specified test parameters
replace_all("photos", "images", "photos/notes.txt", "photos/new_notes.txt")

# 4. Verify the output (optional)
with open("photos/new_notes.txt", "r") as f:
    print("\nContents of photos/new_notes.txt:")
    print(f.read())


