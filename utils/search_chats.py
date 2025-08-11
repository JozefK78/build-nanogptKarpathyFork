import os
import json
import re
from datetime import datetime

# --- Configuration ---
CHAT_DIRECTORY = "chat_data"
MAX_RESULTS = 10
# -------------------

def find_relevant_chats():
    """
    Searches through chat files for specific keywords and prints matching files.
    """
    print(f"Searching for chats in: '{CHAT_DIRECTORY}/'")

    # 1. Check if the chat directory exists
    if not os.path.isdir(CHAT_DIRECTORY):
        print(f"\n--- ERROR ---")
        print(f"The directory '{CHAT_DIRECTORY}' was not found.")
        print("Please make sure you have run the 'copy_chats.py' script first.")
        return

    # 2. Get all files and their modification times
    try:
        all_files = [os.path.join(CHAT_DIRECTORY, f) for f in os.listdir(CHAT_DIRECTORY) if os.path.isfile(os.path.join(CHAT_DIRECTORY, f))]
        # Sort files by modification time, newest first
        all_files.sort(key=lambda x: os.path.getmtime(x), reverse=True)
    except Exception as e:
        print(f"Error reading files from directory: {e}")
        return

    print(f"Found {len(all_files)} files. Searching for matches...")
    print("-" * 20)

    # 3. Define search patterns (case-insensitive)
    # Pattern for 'gpt2' or 'gpt-2' or 'fineweb'
    topic_pattern = re.compile(r'gpt-?2|fineweb', re.IGNORECASE)
    # Pattern for 'learning plan'
    action_pattern = re.compile(r'learning plan', re.IGNORECASE)

    # 4. Iterate through files and search for matches
    found_count = 0
    for file_path in all_files:
        if found_count >= MAX_RESULTS:
            print(f"\nReached maximum of {MAX_RESULTS} results. Stopping.")
            break
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
                # Extract text from the JSON structure
                full_text = ""
                if 'chunkedPrompt' in data and 'chunks' in data['chunkedPrompt']:
                    for chunk in data['chunkedPrompt']['chunks']:
                        if 'text' in chunk:
                            full_text += chunk['text'] + "\n"
                
                # Search for both patterns in the extracted text
                if topic_pattern.search(full_text) and action_pattern.search(full_text):
                    found_count += 1
                    mod_time = datetime.fromtimestamp(os.path.getmtime(file_path))

                    # Check which specific topics were found for detailed reporting
                    found_topics = []
                    if re.search(r'gpt-?2', full_text, re.IGNORECASE):
                        found_topics.append('gpt2')
                    if re.search(r'fineweb', full_text, re.IGNORECASE):
                        found_topics.append('fineweb')

                    print(f"  [{found_count}] Match found: {os.path.basename(file_path)}")
                    print(f"      (Date: {mod_time.strftime('%Y-%m-%d %H:%M:%S')})")
                    print(f"      (Topics: {', '.join(found_topics)})")

        except json.JSONDecodeError:
            # This might happen if a file is not a valid JSON
            # print(f"Warning: Could not parse JSON from '{os.path.basename(file_path)}'. Skipping.")
            continue
        except Exception as e:
            print(f"An error occurred while processing {os.path.basename(file_path)}: {e}")

    print("-" * 20)
    if found_count == 0:
        print("No matching chat files were found.")
    else:
        print(f"Search complete. Found {found_count} matching files.")


if __name__ == "__main__":
    find_relevant_chats()