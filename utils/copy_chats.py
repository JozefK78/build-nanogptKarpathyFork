import os
import shutil
import glob

# --- Configuration ---
# IMPORTANT: Please verify this is the correct path to your Google AI Studio files.
# If your Google Drive has a different letter or path, update this variable.
SOURCE_DRIVE_PATH = r"G:\My Drive\Google AI Studio"

# This is the destination in your current project folder.
DESTINATION_PATH = os.path.join(os.getcwd(), "chat_data")
# -------------------

def copy_chat_files():
    """
    Finds and copies chat files from the source to the destination directory.
    """
    print(f"Source directory: {SOURCE_DRIVE_PATH}")
    print(f"Destination directory: {DESTINATION_PATH}")

    # 1. Check if the source directory exists
    if not os.path.isdir(SOURCE_DRIVE_PATH):
        print(f"\n--- ERROR ---")
        print(f"The source directory was not found: '{SOURCE_DRIVE_PATH}'")
        print("Please make sure the path is correct in the `SOURCE_DRIVE_PATH` variable inside this script.")
        return

    # 2. Create the destination directory if it doesn't exist
    os.makedirs(DESTINATION_PATH, exist_ok=True)
    print(f"Ensured destination directory exists.")

    # 3. Find all files in the source directory
    search_pattern = os.path.join(SOURCE_DRIVE_PATH, '*')
    all_files = [f for f in glob.glob(search_pattern) if os.path.isfile(f)]

    if not all_files:
        print("\n--- WARNING ---")
        print(f"No files were found in '{SOURCE_DRIVE_PATH}'.")
        print("Please check the directory.")
        return

    # 4. Copy the files
    print(f"\nFound {len(all_files)} files. Starting copy...")
    copied_count = 0
    skipped_count = 0
    for idx, src_path in enumerate(all_files):
        try:
            # Sanitize filename: replace colon with underscore
            original_filename = os.path.basename(src_path)
            sanitized_filename = original_filename.replace(":", "_")
            dest_path = os.path.join(DESTINATION_PATH, sanitized_filename)

            # Check if file exists and if it's identical
            if os.path.exists(dest_path):
                src_stat = os.stat(src_path)
                dest_stat = os.stat(dest_path)
                # Compare modification time and size
                if src_stat.st_mtime == dest_stat.st_mtime and src_stat.st_size == dest_stat.st_size:
                    # print(f"  ({idx + 1}/{len(all_files)}) Skipping '{file_name}' (already exists and is identical).")
                    skipped_count += 1
                    continue

            print(f"  ({idx + 1}/{len(all_files)}) Copying '{sanitized_filename}'...")
            shutil.copy2(src_path, dest_path) # copy2 preserves metadata like modification time
            copied_count += 1
        except Exception as e:
            print(f"  - ERROR copying file {sanitized_filename}: {e}")
    
    print(f"\nCopy complete. Copied: {copied_count}, Skipped: {skipped_count}, Total: {len(all_files)}")

    # 5. Verify by listing files in the destination directory
    print("\n--- Files in destination directory ---")
    final_files = os.listdir(DESTINATION_PATH)
    if final_files:
        for item in final_files[:10]: # Print first 10
            print(f"- {item}")
        if len(final_files) > 10:
            print(f"...and {len(final_files) - 10} more.")
    else:
        print("No files were found in the destination directory.")


if __name__ == "__main__":
    copy_chat_files()
