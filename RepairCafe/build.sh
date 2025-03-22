#!/usr/bin/env bash
# Exit on error
set -o errexit

# Modify this line as needed for your package manager (pip, poetry, etc.)
pip install -r requirements.txt

# Convert static asset files
python manage.py collectstatic --no-input

# Apply any outstanding database migrations
python manage.py makemigrations RepairCafe
python manage.py showmigrations
python manage.py migrate
python manage.py 
python manage.py populate_RepairCafe.py
