#!/bin/bash

# Find all Python files in the producers directory and run them in parallel
for script in producers/*.py; do
    python "$script" &
done

# Wait for all background processes to complete
wait