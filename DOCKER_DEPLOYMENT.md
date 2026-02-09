# Docker Deployment Guide (Personal Use)

Simple Docker Compose setup for personal use with SQLite.

## Quick Start

### 1. Build and start the container

```bash
docker-compose up -d --build
```

### 2. Create a superuser

```bash
docker-compose exec web python manage.py createsuperuser
```

### 3. Access the application

Visit `http://localhost:8000` in your browser (or your VPN IP:8000)

## Management Commands

### View logs
```bash
docker-compose logs -f
```

### Stop container
```bash
docker-compose down
```

### Restart container
```bash
docker-compose restart
```

### Create superuser
```bash
docker-compose exec web python manage.py createsuperuser
```

### Access Django shell
```bash
docker-compose exec web python manage.py shell
```

### Access container shell
```bash
docker-compose exec web bash
```

## Data Persistence

Your SQLite database is stored in a Docker volume named `sqlite_data`, so your data persists even if you stop/restart containers.

To completely remove everything including data:
```bash
docker-compose down -v
```

## Accessing from VPN

The app is accessible at `http://YOUR_VPN_IP:8000`

If you want to change the port, edit `docker-compose.yml`:
```yaml
ports:
  - "YOUR_PORT:8000"
```

## Troubleshooting

### Container won't start
```bash
docker-compose logs web
```

### Permission errors
```bash
docker-compose down
docker-compose up -d --build
```

## Local Development (without Docker)

You can still run locally:
```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```
