#!/bin/bash

# Create the txts directory if it doesn't exist
mkdir -p txts

# Find all .py and .ipynb files in the current directory
for file in *.py *.ipynb; do
  # Check if the file exists to avoid errors if no files of a certain type are found
  if [ -f "$file" ]; then
    # Define the new filename
    new_filename="${file}.txt"
    # Copy the file to the txts directory with the new name
    cp "$file" "txts/$new_filename"
    echo "Copied $file to txts/$new_filename"
  fi
done

echo "Processing complete."