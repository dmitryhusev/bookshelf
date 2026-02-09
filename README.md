# Bookshelf - Lightweight Django Goodreads Clone

A simple, clean Django app for tracking books with Goodreads-like functionality.

## Features

- 📚 Browse and search books
- 📝 Write reviews (no ratings)
- 📖 Three reading shelves: Want to Read, Currently Reading, Read
- ➕ Add new books
- ✏️ Edit and delete books
- 🔍 Search by title or author

## Quick Start with Docker (Recommended)

### Prerequisites
- Docker and Docker Compose installed

### 1. Start the application

```bash
docker compose up -d --build
```

### 2. Create a superuser

```bash
docker compose exec web python manage.py createsuperuser
```

### 3. Access the application

Visit `http://localhost:8000` in your browser!

### Management Commands

**View logs:**
```bash
docker compose logs -f
```

**Stop the application:**
```bash
docker compose down
```

**Restart the application:**
```bash
docker compose restart
```

**Access Django shell:**
```bash
docker compose exec web python manage.py shell
```

**Create additional users:**
Use the admin panel at `http://localhost:8000/admin`

### Accessing from VPN

If you're running this on a VPN server, access it at:
```
http://YOUR_VPN_IP:8000
```

To change the port, edit `docker compose.yml`:
```yaml
ports:
  - "YOUR_PORT:8000"
```

## Local Development (Without Docker)

### 1. Install Django

```bash
pip install django
```

### 2. Set up the database

```bash
python manage.py migrate
```

### 3. Create a superuser

```bash
python manage.py createsuperuser
```

### 4. Run the development server

```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000` to see your app!

## Usage

### Admin Panel
- Visit `http://localhost:8000/admin` to manage books and users
- Create additional user accounts here

### Features
- **Browse Books**: View all books in the library
- **Search**: Find books by title or author
- **Shelves**: Organize books into Want to Read, Currently Reading, or Read
- **Reviews**: Write and read reviews for any book
- **Add Books**: Contribute new books to the library
- **Edit Books**: Update book information (title, author, cover URL, etc.)
- **Delete Books**: Remove books from the library

## Project Structure

```
bookshelf/              # Main app
├── models.py           # Book, Shelf, Review models
├── views.py            # All view logic
├── forms.py            # Review and Book forms
├── urls.py             # URL routing
├── admin.py            # Admin configuration
└── templates/          # HTML templates

config/                 # Project settings
├── settings.py
└── urls.py

Dockerfile              # Docker configuration
docker compose.yml      # Docker Compose setup
manage.py              # Django management script
```

## Models

- **Book**: title, author, description, cover_url, isbn, published_year
- **Shelf**: user, book, shelf_type (want_to_read/currently_reading/read)
- **Review**: user, book, content

## Data Persistence

When running with Docker, your SQLite database is stored in a Docker volume, so your data persists even when you stop/restart containers.

To completely remove everything including data:
```bash
docker compose down -v
```

## Troubleshooting

### Docker container won't start
```bash
docker compose logs web
```

### Need to rebuild after code changes
```bash
docker compose down
docker compose up -d --build
```

## Customization

- Modify templates in `bookshelf/templates/bookshelf/`
- Update styles in `base.html`
- Change settings in `config/settings.py`

Enjoy your reading! 📚
