# Week 12 Project Japan 47

A community-driven travel platform built with Django that helps people discover Japan through its 47 prefectures.

Visitors can explore regions, prefectures, and places, while registered users can contribute new destinations, write reviews, build a public profile, and earn contributor badges.

This project was built as the final project for Week 12 of my Django learning roadmap, combining everything learned throughout the first twelve weeks into one complete web application.

---

## Features

### Travel Discovery

- Browse all 9 regions of Japan
- Explore all 47 prefectures
- Discover community-submitted places
- Search, filter, and sort places
- View detailed place pages with images and descriptions

### Community

- User registration and authentication
- Public contributor profiles
- User profile images
- Nickname support
- Place reviews and ratings
- Contributor points and badge progression

### Moderation

- User-submitted places require staff approval
- Published and unpublished place management
- Owner permissions for editing and deleting content

### Ratings

Hierarchical rating system:

- Reviews determine Place ratings
- Place ratings determine Prefecture ratings
- Prefecture ratings determine Region ratings

Each place contributes equally to its prefecture rating, regardless of how many reviews it has received.

### AI Helper

A floating AI assistant is available throughout the website.

The helper is powered by the OpenAI Responses API and is configured specifically to answer questions about the Japan 47 website.

---

## Technology

- Python 3.12+
- Django 6.0
- SQLite (development)
- Pillow
- pillow-heif
- OpenAI Responses API
- HTML
- CSS
- Vanilla JavaScript

---

## Local Setup

### 1. Clone the repository

```bash
git clone <repository-url>
cd "Week 12 Project Japan 47"
```

### 2. Create a virtual environment

```bash
python3 -m venv .venv
```

Linux / macOS:

```bash
source .venv/bin/activate
```

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Create a local environment file

```bash
cp .env.example .env
```

Add your own OpenAI API key.

Never commit `.env`.

Generate a secure `DJANGO_SECRET_KEY` before deployment.

### 5. Run Django

```bash
cd japan_47

python manage.py migrate

python manage.py createsuperuser

python manage.py runserver
```

Open:

```
http://127.0.0.1:8000/
```

Admin:

```
http://127.0.0.1:8000/admin/
```

---

## AI Helper Configuration

The floating assistant uses the OpenAI Responses API.

The API key remains on the server and is never exposed to browser JavaScript.

Environment variables:

| Variable | Default | Purpose |
|----------|---------|---------|
| OPENAI_MODEL | gpt-5-mini | AI model |
| OPENAI_TIMEOUT_SECONDS | 12 | Request timeout |
| OPENAI_MAX_OUTPUT_TOKENS | 500 | Maximum response length |
| CHATBOT_MAX_INPUT_CHARACTERS | 800 | Maximum question length |
| CHATBOT_RATE_LIMIT_SECONDS | 5 | Minimum delay between requests |
| CHATBOT_RATE_LIMIT_REQUESTS | 20 | Requests allowed during one window |
| CHATBOT_RATE_LIMIT_WINDOW | 3600 | Rate-limit window |

The browser timeout is 15 seconds.

For production deployments, use a shared cache such as Redis instead of Django's local memory cache.

---

## Running Tests

From the `japan_47` directory:

```bash
python manage.py check

python manage.py test
```

OpenAI requests are mocked during testing and do not consume API credits.

---

## Project Structure

```text
Week 12 Project Japan 47/
├── .env.example
├── requirements.txt
├── README.md
└── japan_47/
    ├── manage.py
    ├── japan_47/
    ├── travel/
    └── media/
```

---

## Repository Safety

The repository excludes:

- uploaded media
- local SQLite database
- virtual environments
- cache files
- editor settings
- log files
- local environment variables

The repository keeps:

- logo
- favicon
- contributor badges
- other static project assets

under:

```
travel/static/images/
```

---

## Future Improvements

A roadmap of planned improvements is available in:

```
PROJECT_ROADMAP.md
```

The project will continue to evolve after the Django learning roadmap is completed, with additional features, deployment, performance improvements, and UI polishing.

---

## Deployment Notes

Before deployment:

- Disable DEBUG
- Configure ALLOWED_HOSTS
- Set production environment variables
- Configure PostgreSQL (or another production database)
- Configure shared caching
- Configure static and media file serving
- Rotate any previously exposed secrets
- Run Django deployment checks

```bash
python manage.py check --deploy
```