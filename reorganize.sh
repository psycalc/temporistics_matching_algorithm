#!/bin/bash

# Navigate to your project directory
cd ~/projects/psycalc/temporistics_matching_algorithm

# Create the necessary directories
mkdir -p app/static/css
mkdir -p app/templates
mkdir -p app/typologies

# Move the typologies python files
mv typologies/*.py app/typologies/

# Create __init__.py files to mark directories as packages
touch app/__init__.py
touch app/typologies/__init__.py

# Create a basic routes.py file
cat <<EOL > app/routes.py
from flask import render_template
from app import app

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')
EOL

# Create a basic run.py file
cat <<EOL > run.py
from app import app

if __name__ == '__main__':
    app.run(debug=True)
EOL

# Create a basic config.py file
touch config.py

# Create basic HTML templates
cat <<EOL > app/templates/index.html
<!DOCTYPE html>
<html>
<head>
    <title>Relationship Calculator</title>
</head>
<body>
    <!-- Your content here -->
</body>
</html>
EOL

cat <<EOL > app/templates/result.html
<!DOCTYPE html>
<html>
<head>
    <title>Result</title>
</head>
<body>
    <!-- Your result here -->
</body>
</html>
EOL

# Optional: clean up
find . -name '__pycache__' -exec rm -rf {} +

# Output the new directory structure to confirm
tree
