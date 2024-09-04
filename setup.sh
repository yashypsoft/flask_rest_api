# Create a virtual environment
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate

# Install required packages
pip install Flask Flask-MySQL Flask-Migrate Prometheus-Flask-Exporter

pip freeze > requirements.txt
