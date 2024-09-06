source venv/bin/activate
docker-compose up -d --build
docker-compose exec web flask db init
docker-compose exec web flask db migrate -m "Initial migration."
docker-compose exec web flask db upgrade
