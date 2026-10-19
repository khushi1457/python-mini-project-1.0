#!/bin/bash
# Move to the project directory
cd "$(dirname "$0")"

# Launch the Climate-Smart Agricultural Decision System
python3 agri_system_app.py "$@"
