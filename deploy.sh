#!/bin/bash
cd ~/src
git pull
cp app.py ~/flaskapp/__init__.py
cp questions.py ~/flaskapp/
cp templates/*.html ~/flaskapp/templates/
cp -r static ~/flaskapp/
sed -i '1i import sys, os\nsys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))' ~/flaskapp/__init__.py
echo 'application = app' >> ~/flaskapp/__init__.py
~/flaskapp/env/bin/pip install -r requirements.txt
