#!/bin/bash

# Define the directory I want to check for updates and archive name
ref_dir="/content"
archive_name="content.tar.gz"

# Get the creation date of the reference file
# Disclaimer GetFileInfo is only available on MacOS
# Use `stat -c %y file_name instead if on Linux`
ref_date=$(GetFileInfo -d $ref_dir)

echo "Checking for files that were updated after $ref_date"

# Use the find command to find all files updated after the reference date
find . -type f -newermt "$ref_date" -name *.gmi > updated_files.txt

# Display how many new .gmi files were found
file_count=$(wc -l < updated_files.txt)
echo "Number of updated files found: $file_count"

# Archive the files using the tar command
tar -zcf "$archive_name" -T updated_files.txt

# Remove the temporary file
rm updated_files.txt

# Upload file to the capsule
scp content.tar.gz user@host:/content/directory
