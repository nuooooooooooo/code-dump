#!/bin/bash

capsule_name="example.com"

# Check if the archive exists
if [ -f /content/content.tar.gz ]; then
  # Open the archive if it exists
  tar -xf /content/content.tar.gz && rm content.tar.gz
  echo "$capsule_name: Capsule updated"
else
  # Print an error message if the archive does not exist
  echo "$capsule_name: No new files found"
fi
